class User:
    def __init__(self, user_name: str, password: str):
        if isinstance(user_name, str):
            self.__user_name = user_name.strip().lower()
        else:
            self.__user_name = None
        if isinstance(password, str):
            self.__password = password
        else:
            self.__password = None
        self.__watched_movies = []
        self.__reviews = []
        self.__time_spent_watching_movies_minutes = 0

    @property
    def user_name(self):
        return self.__user_name

    @user_name.setter
    def user_name(self, user_name):
        if isinstance(user_name, str):
            self.__user_name = user_name.strip().lower()
        else:
            self.__user_name = None

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        if isinstance(password, str):
            self.__password = password
        else:
            self.__password = None

    @property
    def watched_movies(self):
        return self.__watched_movies

    @watched_movies.setter
    def watched_movies(self, watched_movies):
        if isinstance(watched_movies, list):
            new_list = []
            self.__time_spent_watching_movies_minutes = 0
            for w in watched_movies:
                if isinstance(w, Movie):
                    if w not in new_list:
                        new_list.append(w)
                    if w.runtime_minutes != None:
                        self.__time_spent_watching_movies_minutes += w.runtime_minutes
            self.__watched_movies = new_list

    @property
    def reviews(self):
        return self.__reviews

    @reviews.setter
    def reviews(self, reviews):
        if isinstance(reviews, list):
            new_list = []
            for r in reviews:
                if isinstance(r, Review):
                    if r not in new_list:
                        new_list.append(r)
            self.__reviews = new_list

    @property
    def time_spent_watching_movies_minutes(self):
        return self.__time_spent_watching_movies_minutes

    @time_spent_watching_movies_minutes.setter
    def time_spent_watching_movies_minutes(self, time_spent_watching_movies_minutes):
        if isinstance(time_spent_watching_movies_minutes, int) and time_spent_watching_movies_minutes >= 0:
            self.__time_spent_watching_movies_minutes = time_spent_watching_movies_minutes

    def __repr__(self):
        return f'<User {self.__user_name}>'

    def __eq__(self, other):
        if isinstance(other, User):
            return False
        return self.__user_name == other.user_name

    def __lt__(self, other):
        if isinstance(other, Movie):
            return self.__user_name < other.user_name

    def __hash__(self):
        return hash(self.__user_name)

    def watch_movie(self, movie):
        if isinstance(movie, Movie):
            if movie not in self.__watched_movies:
                self.__watched_movies.append(movie)
                if movie.runtime_minutes != None:
                    self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review):
        if isinstance(review, Review):
            if review not in self.__reviews:
                self.__reviews.append(review)