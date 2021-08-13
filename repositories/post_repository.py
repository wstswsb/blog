from datetime import datetime
from translators.post_tranlator import PostTranslator
from typing import Any
from pymongo import MongoClient
from bson import ObjectId
from repositories.repository import Repository
from models.post import Post


class PostRepository(Repository):
    def __init__(self, client: MongoClient, translator: PostTranslator):
        super().__init__(translator)
        self.client = client
        self.collection = client.blog_database.posts

    def get_pages(self,
                  page_number: int,
                  page_size: int
                  ) -> list[Post]:

        posts = list(self.collection.find().sort('_id', -1)
                     .skip(page_number*page_size - page_size)
                     .limit(page_size))
        posts = [
            self.translator.from_document(post)
            for post in posts
            if post is not None
        ]
        return posts

    def get_by_id(self, post_id: ObjectId) -> Any:
        post = self.collection.find_one({"_id": post_id})
        if post is None:
            return None
        else:
            return self.translator.from_document(post)

    def delete_by_id(self, post_id: ObjectId) -> bool:
        if not isinstance(post_id, ObjectId) or not self.is_exists(post_id): 
            return False

        self.collection.delete_one({'_id': post_id})
        return True

    def create(self, text: str, author: str) -> ObjectId:
        if not isinstance(text, str) or not isinstance(author, str):
            return None
        post = Post(text=text, author=author, date_of_creation=datetime.now())
        created_id = self.collection.insert_one(
                self.translator.to_document(post)).inserted_id
        return created_id 

    def update(self, post_id: ObjectId, text: str, author: str) -> Post:
        if not isinstance(post_id,  ObjectId) or \
                    not isinstance(text, str) or \
                    not isinstance(author, str):
           return None 

        if not self.is_exists(post_id):
            return None    
        self.collection.update_one({'_id': ObjectId(post_id)},
                                   {"$set": {"text": text, "author": author}})
        return self.get_by_id(post_id)
    

    def is_exists(self, post_id: ObjectId) -> bool:
        if not isinstance(post_id, ObjectId):
            return False
        
        if self.get_by_id(post_id):
            return True
        
        return False

if __name__ == "__main__":
    MONGO_HOST = "localhost"
    MONGO_PORT = 27017
    mongo_client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")

    post_repo = PostRepository(mongo_client)
    print(post_repo.get_by_id('asd'))
