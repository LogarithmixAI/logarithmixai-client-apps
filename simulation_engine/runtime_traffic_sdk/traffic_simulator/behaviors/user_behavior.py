class UserBehavior:

    def __init__(self, session_gen):

        self.session_gen = session_gen
        self.think_time = self.session_gen.think_time
        self.sessions = []
        

    def activate(self):

        session = self.session_gen.activate_user()
        if not session:
            return None
        
        self.sessions.append(session)
        
        return session

    def identity(self,session):
        if session in self.sessions:
            return {
                "user_id": session.user_id,
                "session_id": session.id
            }
        return {
                "user_id": none,
                "session_id": none
            }

    def next_action(self, session):
        if session in self.sessions:
            endpoint = session.next_request()
            return endpoint, "GET"
        return "/", "GET"

    def deactivate(self, session):
        if session in self.sessions:
            self.session_gen.deactivate_user(session.user)
            self.sessions.remove(session)
            
