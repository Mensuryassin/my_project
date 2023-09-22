from flask_app.config.mysqconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash


class Video:
    db = "project_schema"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.genre = data['genre']
        self.description =  data['description']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
        self.first_name = data["first_name"]

    @classmethod
    def save(cls, data):
        query = "INSERT INTO videos(title, genre, description, date_made, user_id) VALUES(%(title)s, %(genre)s, %(description)s, %(date_made)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM videos Join users on videos.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query, data)
        all_videos = []
        for row in results:
            video = cls(row)
            user_data = {
                "id":row['users.id'],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : None,
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]
            }
            user_instance = User(user_data)
            video.user = user_instance
            print(row["description"])
            all_videos.append(cls(row))
        return all_videos
    
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM videos JOIN users on videos.user_id = users.id WHERE videos.id = %(id)s"
        video_dict = connectToMySQL(cls.db).query_db(query, data)
        print(video_dict)

        video_obj = Video(video_dict[0])
        user_obj = User({
            "id" : video_dict[0]["id"],
            "first_name" : video_dict[0]["first_name"],
            "last_name" : video_dict[0]["last_name"],
            "email" : video_dict[0]["email"],
            "password" : video_dict[0]["password"],
            "created_at" : video_dict[0]["created_at"],
            "updated_at" : video_dict[0]["updated_at"]
        })
        video_obj.user = user_obj
        return video_obj

    
    @classmethod
    def update(cls, data):
        query ="""UPDATE videos SET title=%(title)s, genre=%(genre)s, description=%(description)s, 
        date_made=%(date_made)s,updated_at=NOW() WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    
    @classmethod
    def destroy(cls, data):  
        query = "DELETE FROM videos WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    
    @staticmethod
    def valid_video(video):
        is_valid = True
        if len(video['title']) < 2:
            is_valid = False
            flash ("title must be at least 3 characters", "video")
        if len(video['genre']) < 3:
            is_valid = False
            flash ("genre must be  at least 3 characters", "video")
        if len(video['description']) < 10:
            is_valid = False
            flash ("description must be  at least 10 characters", "video")
        if len(video['date_made']) =="":
            is_valid = False
            flash ("Please enter a date", 'video')
        return is_valid