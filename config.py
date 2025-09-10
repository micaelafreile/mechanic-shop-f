class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:newpassword@localhost/mechanic_shop_f' 
    DEBUG = True


class TestingConfig:
    pass
class ProductionConfig:
    pass