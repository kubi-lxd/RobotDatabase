import pymongo
import threading
from mongoengine import *
from datetime import datetime
from registry import registered_env, registered_urdf, registered_sensor


class Mongo:
    def __init__(self, host, port, username, password):

        self.client = pymongo.MongoClient('mongodb://' + username + ':' + password + '@' + host + ':' + str(port))

        self.db = None
        self.urdf = ''
        self.sensor_lists = []
        self.env = ''

        self.collection_demonstration = None
        self.collection_sensor = None
        self.collection_control = None
        self.collection_control_model = None
        self.collection_human = None

    def create_database(self, urdf, sensors, env):
        assert urdf in registered_urdf.keys(), 'urdf model is not registered, please check model name'
        assert [sensor for sensor in sensors if sensor in registered_sensor.keys()], 'some sensors are not registered'
        assert env in registered_env.keys(), 'gym environment is not registered, please check model name'
        database_name = urdf+'_'.join(sensors)+env
        self.urdf = urdf
        self.sensor_lists = sensors
        self.env = env
        self.db = self.client[database_name]
        return database_name

    def create_collections(self):
        self.collection_demonstration = self.db['demonstration']
        self.collection_sensor = self.db['sensor']
        self.collection_control = self.db['control']
        self.collection_control_model = self.db['control_model']
        self.collection_human = self.db['human']


class Sensors(EmbeddedDocument):
    # 用于存储连续传感数据的文档
    sensor_choice = (
        "MonocularFPV",
        "MonocularTPV",
        "BinocularFPV",
        "BinocularTPV",
        "DepthVision",
        "MultiocularVision",
        "EyeTracking",
        "Voice",
        "Force",
        "PointCloud",
        "Sound",
        "MultiIMU",
        "Radar",
    )
    type = StringField(required=True, choices=sensor_choice)
    sensor = ListField(GenericEmbeddedDocumentField, required=True)
    meta = {"collection": "Sensors"}


class Sensor(EmbeddedDocument):
    # 传感器数据主类
    index = IntField(required=True)
    date = DateTimeField(required=True)  # 传感时间
    meta = {"collection": "Sensor", 'allow_inheritance': True}


class SensorMonocularFPV(Sensor):
    # 传感器某一帧数据
    type = StringField('Image')
    data = ImageField(size=(800, 600, True), required=True)
    meta = {'allow_inheritance': True}


class SensorMonocularTPV(SensorMonocularFPV):
    pass


class SensorBinocularFPV(Sensor):
    # 传感器某一帧数据
    type = StringField('Images')
    data = ImageField(size=(800, 600, True), required=True)
    data_another = ImageField(size=(800, 600, True), required=True)
    meta = {'allow_inheritance': True}


class SensorBinocularTPV(SensorBinocularFPV):
    pass


class SensorDepthVision(SensorMonocularFPV):
    pass


class SensorMultiocularVision(Sensor):
    type = StringField('Images')
    sensor_num = IntField(required=True)
    data = ListField(ImageField(size=(800, 600, True), required=True))


class SensorEyeTracking(Sensor):
    type = StringField('SensorEyeTracking')
    rawdata = ImageField(size=(800, 600, True), required=True)
    data = ListField(FloatField(required=True))


class SensorFile(Sensor):
    data = FileField(required=True)
    meta = {'allow_inheritance': True}


class SensorVoice(SensorFile):  # 语音
    type = StringField('Voice')


class SensorSound(SensorFile):  # 超声波等声音
    type = StringField('Sound')


class SensorPointCloud(SensorFile):
    type = StringField('PCD')


class SensorRadar(SensorFile):
    type = StringField('Pcap')


class SensorSignal(Sensor):
    data = ListField(FloatField(required=True))
    meta = {'allow_inheritance': True}


class SensorForce(SensorSignal):
    type = StringField('Force')


class SensorIMU(SensorSignal):
    type = StringField('MultiIMU')


class Human(EmbeddedDocument):
    # 人类数据主类
    index = IntField(required=True)
    date = DateTimeField(required=True)  # 传感时间
    meta = {"collection": "Human", 'allow_inheritance': True}


class HumanBVH(Human):
    type = StringField('BVH')
    rawdata = FileField(required=True)
    data = DictField(required=True)


class HumanOpenPose(Human):
    type = StringField('Openpose')
    rawdata = ListField(FileField(required=True))  # TODO:存储图片存储文件区别 ？
    data = DictField(required=True)


class HumanPoseEstimation(Human):
    type = StringField('HumanPoseEstimation')
    rawdata = ListField(FileField(required=True))
    data = DictField(required=True)


class Control(EmbeddedDocument):
    # 控制输出数据
    index = IntField(required=True)
    date = DateTimeField(required=True)  # 传感时间
    meta = {"collection": "Control", 'allow_inheritance': True}


class ControlEnd(Control):
    type = StringField('End Control')
    data = ListField(required=True)


class ControlJoints(EmbeddedDocument):
    type = StringField('Joints Control')
    joint_num = IntField(required=True)
    joint_list = ListField(required=True)
    data = ListField(required=True)


class ControlNatural(EmbeddedDocument):
    type = StringField('Natural Teaching')
    joint_num = IntField(required=True)
    joint_list = ListField(required=True)
    data = ListField(required=True)


class ControlModel(EmbeddedDocument):
    # 模型数据
    date = DateTimeField(required=True)  # 时间
    name = StringField(default="", max_length=200)  # 模型简名
    description = StringField(default="", max_length=200)  # 注释 备注这个模型是做什么的
    mapping = DictField(required=True)  # 自由度与控制序号映射关系
    model = DictField(required=True)  # 实际上是一个输入对应一个什么样的输出控制量 TODO：这里工作量比较大
    meta = {"collection": "ControlModel"}


class Demonstration(Document):
    # 一次示教的根文档
    name = StringField(required=True, max_length=200)
    date = DateTimeField(default=datetime.now(), required=True)  # 示教创建时间
    description = StringField(default="", max_length=200)  # 注释 备注这个示教是做什么的
    length = IntField(default=0)  # 每插入一次数据加1
    sensor_num = IntField(required=True)
    sensors_type_list = ListField(StringField(max_length=10), required=True, primary_key=False)  # 准备插入的传感器类型列表
    sensors = ListField(EmbeddedDocumentField('Sensors'), required=True)
    human = ListField(GenericEmbeddedDocumentField('Human'), required=True)
    control = ListField(GenericEmbeddedDocumentField('Control'), required=True)
    control_model = GenericEmbeddedDocumentField('ControlModel')
    meta = {"collection": "Demonstration"}


if __name__ == '__main__':
    mongo = Mongo('127.0.0.1', 27017, 'SRL', '213')
    dbname = mongo.create_database('Inmoov', ['MonocularFPV', 'MonocularFPV'], 'JakaGymEnv-v0')
    mongo.create_collections()
    connect('dbname', host='127.0.0.1', username='SRL', password='213')
