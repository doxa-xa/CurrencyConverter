from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+mysqlconnector://newuser:password@localhost:3306/household",
              echo=True, connect_args={'auth_plugin':'mysql_native_password'})

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    __table_args__ = {'schema':'household'}

    project_id = Column(Integer, primary_key=True)
    title = Column(String(length=50))
    description = Column(String(length=50))

    def __repr__(self):
        return f"<Project(title{self.title}, description={self.description})>"
    
class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'schema':'household'}

    task_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('household.projects.project_id'))
    description = Column(String(length=50))

    project = relationship("Project")

    def __repr__(self):
        return f"<Task(description={self.description})>"
    
Base.metadata.create_all(engine)

session_maker = sessionmaker()
session_maker.configure(bind=engine)
session = session_maker()

organize_closet_project = Project(title='Organize Closet',
description="Organize closet by color and style")
session.add(organize_closet_project)
session.commit()

tasks = [Task (project_id = organize_closet_project.project_id,
            description = 'Decide what clothes to donate'),
        Task (project_id = organize_closet_project.project_id,
            description = 'Organize winter clothes'),
        Task (project_id = organize_closet_project.project_id,
            description = 'Organize summer clotes')]

session.bulk_save_objects(tasks)
session.commit()

our_project = session.query(Project).filter_by(title="Organize Closet").first()
print(our_project)

our_tasks = session.query(Task).all()

print(our_tasks)