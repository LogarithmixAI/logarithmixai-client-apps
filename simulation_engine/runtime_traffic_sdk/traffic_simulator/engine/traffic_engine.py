import time
import random
import threading
from traffic_simulator.http.http_client import HTTPClient
from traffic_simulator.traffic_patterns.poisson_arrival import PoissonArrival
from traffic_simulator.traffic_patterns.crawler_pattern import CrawlerPattern

from traffic_simulator.traffic_patterns.diurnal_pattern import DiurnalPattern
from traffic_simulator.traffic_patterns.load_scheduler import LoadScheduler
from traffic_simulator.user_behavior.session_generator import SessionGenerator
from traffic_simulator.endpoints.endpoint_pool import EndpointPool
from traffic_simulator.bots.bot_crawler import BotCrawler

from traffic_simulator.engine.worker_pool import WorkerPool
from traffic_simulator.metrics.metrics_collector import MetricsCollector, MetricsReporter
from traffic_simulator.behaviors.user_behavior import UserBehavior
from traffic_simulator.behaviors.api_behavior import ApiBehavior
from traffic_simulator.behaviors.bot_behavior import BotBehavior


class TrafficEngine:

    def __init__(self, config):

        self.config = config

        self.http_client = HTTPClient(config.base_url)
        self.session_gen = SessionGenerator(config)
        self.pattern = DiurnalPattern(config.request_rate)
        self.scheduler = LoadScheduler(config.load_profile)
        self.CrawlerPattern = CrawlerPattern(config.bot_request_rate)
        self.endpoint_pool = EndpointPool()
        self.metrics = MetricsCollector()
        self.crawler = BotCrawler()
        self.running = False


    def worker(self, thread, behavior, pattern):

        arrival = PoissonArrival(1)

        while self.running:

            rate = pattern.current_rate()
            rate = min(rate, self.config.max_rps)

            if rate > 0:

                arrival.rate = rate

                
                identity = behavior.identity()

                endpoint, method = behavior.next_action()

                delay = random.uniform(self.config.think_time_min, self.config.think_time_max)
                time.sleep(delay)

                response = self.http_client.send_request(
                    endpoint,
                    identity,
                    method,
                    thread
                )

                self.metrics.record(
                    response["latency_ms"],
                    response["status"]
                )

                if self.config.debug:
                    print(endpoint, response)
                    
                interval = max(0.001, arrival.next_interval())
            else:
                interval = 2

            time.sleep(interval)

    def user_worker(self, user_session, thread, behavior):

        session = behavior.activate()

        if not session:
            return

        while self.running:

            identity = behavior.identity(session)

            endpoint, method = behavior.next_action(session)

            response = self.http_client.send_request(
                endpoint,
                identity,
                method,
                thread + user_session
            )

            self.metrics.record(
                response["latency_ms"],
                response["status"]
            )

            if self.config.debug:
                print(endpoint, response)

            if behavior.think_time:
                time.sleep(behavior.think_time())

            if session.expired():
                print(f'session deactivate : thread - {thread + user_session}, user_session:{user_session}')
                behavior.deactivate(session)
                active = len(behavior.session_gen.active_users)
                print(f'active_user : {active} | worker: {thread}')
                time.sleep(random.uniform(1,6))
                break

    def arrival_loop(self, thread, behavior, pattern):

        while self.running:

            user_limit = int(pattern.current_rate())

            active = len(behavior.session_gen.active_users)

            user_need = max(user_limit - active, 0)

            for idx in range(user_need):

                t = threading.Thread(
                    target=self.user_worker,
                    args=(f'_{idx}',thread, behavior),
                    daemon=True
                )
                t.start()
                print(f'rate: {user_limit} | active_user: {active} | Require_user : {user_need} | thread: {thread}')

            time.sleep(1)

    def start(self):

        print("Traffic engine started")
        self.running = True

        user_pattern = self.pattern
        api_pattern = self.scheduler
        bot_pattern = self.CrawlerPattern  # temporary

        pool_user = WorkerPool(self.config.user_workers, lambda t: self.arrival_loop(f'user_worker_{t}', UserBehavior(SessionGenerator(self.config)), user_pattern))
        pool_api = WorkerPool(self.config.api_workers, lambda t: self.worker(f'api_worker_{t}', ApiBehavior(self.endpoint_pool), api_pattern))
        pool_bot = WorkerPool(self.config.bot_workers, lambda t: self.worker(f'bot_worker_{t}', BotBehavior(self.crawler), bot_pattern))

        pool_user.start()
        pool_api.start()
        pool_bot.start()

        reporter = MetricsReporter(self.metrics)

        reporter_thread = threading.Thread(
            target=reporter.start,
            daemon=True
        )

        reporter_thread.start()

        time.sleep(self.config.duration)

        self.running = False
        reporter.running = False

        pool_user.join()
        pool_api.join()
        pool_bot.join()

        print("Traffic engine stopped")