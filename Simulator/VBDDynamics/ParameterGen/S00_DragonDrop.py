from M01_Parameters import *
from M02_GenRunningParameters import *

if __name__ == "__main__":
    genFileName = Path(__file__).stem

    machineName = "AnkaPC00"
    binaryFile = machines[machineName]["binaryFile"]

    # run = False
    run = True

    models = []
    numModels = 1  # 只有一个龙模型

    # 设置模型初始高度
    modelHeight = 10.0

    model = copy.deepcopy(modelExample)
    # 设置龙模型路径
    model["path"] = "${REPO_ROOT}/Data/mesh_models/Dragon/dragon_drop_low.t"
    model["verticesColoringCategoriesPath"] = (
        "${REPO_ROOT}/Data/mesh_models/Dragon/dragon_drop_low.t.vertexColoring.json"
    )
    model["materialName"] = "NeoHookean"
    model["density"] = 50
    model["miu"] = 2e7  # 弹性参数
    model["lmbd"] = 1e8  # 弹性参数

    # 设置模型位置、缩放和初始速度
    model["translation"] = [0, modelHeight, 0]  # 放置在一定高度
    model["scale"] = [1.0, 1.0, 1.0]  # 可根据龙模型大小调整
    model["initialVelocity"] = [0, -5, 0]  # 初始下落速度

    # 设置物理参数
    model["exponentialVelDamping"] = 0.95
    model["constantVelDamping"] = 0.02
    model["frictionDynamic"] = 0.1
    model["dampingHydrostatic"] = 1e-7
    model["dampingDeviatoric"] = 1e-7
    model["frictionEpsV"] = 0.01

    models.append(model)

    modelsInfo = {"Models": models}

    # 设置物理环境参数
    parameters = getPhysicsParametersForTest(parametersExample)
    parameters["PhysicsParams"]["numFrames"] = 3000
    parameters["PhysicsParams"]["worldBounds"] = [[-20, 0, -20], [20, 30, 20]]
    recoveryState = None

    experimentName = "Dragon_Drop_GPU"
    parameters["PhysicsParams"]["gravity"] = [0.0, -10.0, 0.0]
    parameters["CollisionParams"]["allowDCD"] = True
    parameters["CollisionParams"]["allowCCD"] = True
    parameters["PhysicsParams"]["boundaryFrictionDynamic"] = 0.1

    parameters["PhysicsParams"]["useGPU"] = True
    parameters["CollisionParams"]["restPoseCloestPoint"] = True
    parameters["PhysicsParams"]["collisionStiffness"] = 2e7
    parameters["PhysicsParams"]["checkAndUpdateWorldBounds"] = True

    # 输出设置
    parameters["PhysicsParams"]["saveOutputs"] = True
    parameters["ViewerParams"] = {"enableViewer": True}

    # 设置物理求解器参数
    parameters["PhysicsParams"]["numSubsteps"] = 4
    parameters["PhysicsParams"]["iterations"] = 24
    parameters["PhysicsParams"]["useAccelerator"] = True
    parameters["PhysicsParams"]["acceleratorRho"] = 0.94

    # 生成运行参数并执行
    cmd = genRunningParameters2(
        machineName,
        genFileName,
        experimentName,
        modelsInfo,
        parameters,
        exeName=binaryFile,
        runCommand=run,
        recoverState=recoveryState,
    )
