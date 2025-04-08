from M01_Parameters import *
from M02_GenRunningParameters import *

def getModelInfoDragon(modelExample, materialType="NeoHookean"):
    """创建龙模型信息"""
    model = copy.deepcopy(modelExample)
    model['path'] = "${REPO_ROOT}/Data/mesh_models/Dragon/dragon_drop_low.t"
    model['verticesColoringCategoriesPath'] = model['path'] + ".vertexColoring.json"

    # 物理材质参数
    model['miu'] = 1e9
    model['lmbd'] = 1e10
    model['density'] = 100

    if materialType == "NeoHookean":
        model["materialName"] = "NeoHookean"
    else:
        print("Unrecognized material name! Use default material: NeoHookean")
        model["materialName"] = "NeoHookean"

    return model

if __name__ == '__main__':
    genFileName = Path(__file__).stem

    # 设置使用的机器配置
    machineName = "AnkaPC00"
    run = True

    # 创建模型列表
    models = []

    # 添加龙模型
    dragon_model = getModelInfoDragon(modelExample)
    dragon_model['scale'] = [1.0, 1.0, 1.0]
    dragon_model['translation'] = [0, 0.4, 0]
    dragon_model['initialVelocity'] = [0, 0, 0]

    # 添加阻尼和摩擦参数
    dragon_model["dampingHydrostatic"] = 1e-7
    dragon_model["dampingDeviatoric"] = 1e-7
    dragon_model['frictionDynamic'] = 0.15
    dragon_model["exponentialVelDamping"] = 0.95
    dragon_model["constantVelDamping"] = 0.01
    dragon_model["maxVelocityMagnitude"] = 25

    models.append(dragon_model)

    # 创建模型信息
    modelsInfo = {"Models": models}

    # 设置物理参数
    parameters = getPhysicsParametersForTest(parametersExample)
    parameters["PhysicsParams"]["numFrames"] = 600  # 模拟帧数
    parameters["PhysicsParams"]["checkAndUpdateWorldBounds"] = True
    parameters["PhysicsParams"]["worldBounds"] = [
        [-10.0, 0.0, -10.0],
        [10.0, 10.0, 10.0]
    ]

    # 设置碰撞参数
    parameters["CollisionParams"]["allowDCD"] = True
    parameters["CollisionParams"]["allowCCD"] = True
    parameters["CollisionParams"]["restPoseCloestPoint"] = True

    # 设置其他物理参数
    parameters["PhysicsParams"]["ccdBVHRebuildSteps"] = 50
    parameters["PhysicsParams"]["dcdTetMeshSceneBVHRebuildSteps"] = 50
    parameters["PhysicsParams"]["dcdSurfaceSceneBVHRebuildSteps"] = 50
    parameters["PhysicsParams"]["outputRecoveryStateStep"] = 25
    parameters["PhysicsParams"]["boundaryFrictionDynamic"] = 0.1

    # 设置输出格式和优化参数
    parameters["PhysicsParams"]["outputExt"] = "ply"  # 可以是 "ply" 或 "bin"
    parameters["PhysicsParams"]["useGPU"] = True
    parameters["PhysicsParams"]["collisionStiffness"] = 1e10
    parameters["PhysicsParams"]["numSubsteps"] = 2
    parameters["PhysicsParams"]["iterations"] = 60

    # 设置加速器参数
    parameters["PhysicsParams"]["useAccelerator"] = True
    parameters["PhysicsParams"]["acceleratorRho"] = 0.9

    # 是否保存输出和启用可视化
    parameters["PhysicsParams"]["saveOutputs"] = True  # 输出文件
    parameters["ViewerParams"] = {
        "enableViewer": True  # 启用查看器
    }

    # 生成实验配置
    experimentName = "Dragon_Box_Drop"
    cmd = genRunningParameters2(
        machineName,
        genFileName,
        experimentName,
        modelsInfo,
        parameters,
        exeName=machines[machineName]["binaryFile"],
        runCommand=run
    )
