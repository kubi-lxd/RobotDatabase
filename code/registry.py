# 环境注册名
# TODO:添加详细环境信息
registered_env = {
    "KukaButtonGymEnv-v0":            '',#(KukaButtonGymEnv, SRLGymEnv, PlottingType.PLOT_3D, ThreadingType.PROCESS),
    "KukaRandButtonGymEnv-v0":        '',#(KukaRandButtonGymEnv, KukaButtonGymEnv, PlottingType.PLOT_3D, ThreadingType.PROCESS),
    "Kuka2ButtonGymEnv-v0":           '',#(Kuka2ButtonGymEnv, KukaButtonGymEnv, PlottingType.PLOT_3D, ThreadingType.PROCESS),
    "KukaMovingButtonGymEnv-v0":      '',#(KukaMovingButtonGymEnv, KukaButtonGymEnv, PlottingType.PLOT_3D, ThreadingType.PROCESS),
    "MobileRobotGymEnv-v0":           '',#(MobileRobotGymEnv, SRLGymEnv, PlottingType.PLOT_2D, ThreadingType.PROCESS),
    "MobileRobot2TargetGymEnv-v0":    '',#(MobileRobot2TargetGymEnv, MobileRobotGymEnv, PlottingType.PLOT_2D, ThreadingType.PROCESS),
    "MobileRobot1DGymEnv-v0":         '',#(MobileRobot1DGymEnv, MobileRobotGymEnv, PlottingType.PLOT_2D, ThreadingType.PROCESS),
    "MobileRobotLineTargetGymEnv-v0": '',#(MobileRobotLineTargetGymEnv, MobileRobotGymEnv, PlottingType.PLOT_2D, ThreadingType.PROCESS),
    "Baxter-v0":                      '',#(BaxterEnv, SRLGymEnv, PlottingType.PLOT_3D, ThreadingType.NONE),
    "RoboboGymEnv-v0":                '',#(RoboboEnv, SRLGymEnv, PlottingType.PLOT_2D, ThreadingType.NONE),
    "OmnirobotEnv-v0":                '',#(OmniRobotEnv, SRLGymEnv, PlottingType.PLOT_2D, ThreadingType.PROCESS),
    "InmoovGymEnv-v0":                '',
    "InmoovOneArmButtonGymEnv-v0":    '',
    "JakaGymEnv-v0":                  '',
}
# 模型注册名
# TODO:添加模型描述文件
registered_urdf = {
    "Kuka":   '',
    "Inmoov": '',
    "Jaka":   '',
}
# 传感器类型注册名
# TODO:添加传感信息
registered_sensor = {
    "MonocularFPV":        '',
    "MonocularTPV":        '',
    "BinocularFPV":        '',
    "BinocularTPV":        '',
    "DepthVision":         '',
    "MultiocularVision":   '',
    "EyeTracking":         '',
    "Voice":               '',
    "Force":               '',
    "PointCloud":          '',
    "Sound":               '',
    "MultiIMU":            '',
    "Radar":               '',
}
