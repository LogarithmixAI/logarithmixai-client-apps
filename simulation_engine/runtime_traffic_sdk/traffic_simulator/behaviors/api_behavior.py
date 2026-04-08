import uuid
class ApiBehavior:

    def __init__(self, endpoint_pool):
        self.endpoint_pool = endpoint_pool
        self.think_time = None
        self.Api_id = f'Api_{str(uuid.uuid4())}'
    
    def identity(self):
        return{
                    "user_id": self.Api_id,
                    "session_id": None
            }

    def next_action(self):

        endpoint_obj = self.endpoint_pool.next_endpoint()
        return endpoint_obj.path, endpoint_obj.method