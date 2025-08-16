import os
import argparse
import subprocess
from utils.logger import logger

def run_tests(env="test", markers=None, parallel=1, allure_report=False):
    """
    运行测试用例
    :param env: 运行环境，默认test
    :param markers: 测试标记，如"smoke and high"
    :param parallel: 并行数，默认1
    :param allure_report: 是否生成allure报告，默认False
    """
    try:
        # 设置环境变量
        os.environ["TEST_ENV"] = env
        logger.info(f"开始在{env}环境执行测试...")
        
        # 构建命令
        cmd = ["pytest"]
        if markers:
            cmd.extend(["-m", markers])
        if parallel > 1:
            cmd.extend(["-n", str(parallel)])
        
        # 执行命令
        result = subprocess.run(cmd, check=True)
        
        # 生成allure报告
        if allure_report:
            logger.info("生成Allure报告...")
            subprocess.run(
                ["allure", "generate", "reports/allure_results", "-o", "reports/allure_report", "--clean"],
                check=True
            )
            logger.info("Allure报告已生成: reports/allure_report/index.html")
        
        logger.info("测试执行完成")
        return result.returncode
    except subprocess.CalledProcessError as e:
        logger.error(f"测试执行失败: {str(e)}")
        return e.returncode
    except Exception as e:
        logger.error(f"执行测试时发生错误: {str(e)}")
        return 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="运行接口测试")
    parser.add_argument("--env", type=str, default="test", 
                      help="测试环境: dev, test, prod")
    parser.add_argument("--markers", type=str, 
                      help="测试标记，如'smoke and high'")
    parser.add_argument("--parallel", type=int, default=1, 
                      help="并行执行的进程数")
    parser.add_argument("--allure", action="store_true", 
                      help="生成Allure报告")
    
    args = parser.parse_args()
    run_tests(args.env, args.markers, args.parallel, args.allure)
