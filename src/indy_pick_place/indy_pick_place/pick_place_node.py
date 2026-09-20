#!/usr/bin/env python3

import time

import rclpy
from rclpy.logging import get_logger

from geometry_msgs.msg import PoseStamped

from moveit.planning import MoveItPy
from moveit.core.robot_state import RobotState


class Indy7PickPlace:
    def __init__(self):
        self.logger = get_logger("indy7_pick_place")

        # MoveItPy 초기화
        self.robot = MoveItPy(node_name="indy7_pick_place")

        # Indy7 MoveIt planning group
        #
        # 실제 Indy7 설정에서 사용하는 planning group을 확인한 뒤
        # 필요하면 이 값을 수정한다.
        self.arm = self.robot.get_planning_component("indy7")

        self.logger.info("Indy7 MoveItPy initialized.")

    def plan_and_execute(self):
        """
        현재 상태에서 목표 상태까지 경로를 계획하고 실행한다.
        """

        self.logger.info("Planning motion...")

        # 현재 로봇 상태를 시작 상태로 사용
        self.arm.set_start_state_to_current_state()

        # MoveIt에서 정의된 기본 목표 상태 사용
        #
        # 처음에는 predefined state로 통신/실행 여부를 확인한다.
        self.arm.set_goal_state(configuration_name="home")

        plan_result = self.arm.plan()

        if not plan_result:
            self.logger.error("Motion planning failed.")
            return False

        self.logger.info("Planning successful.")
        self.logger.info("Executing trajectory...")

        self.robot.execute(
            plan_result.trajectory,
            controllers=[]
        )

        self.logger.info("Motion execution finished.")

        return True


def main(args=None):
    rclpy.init(args=args)

    robot = None

    try:
        robot = Indy7PickPlace()

        time.sleep(2.0)

        robot.plan_and_execute()

        time.sleep(2.0)

    except Exception as e:
        logger = get_logger("indy7_pick_place")
        logger.error(f"Error: {e}")

    finally:
        if robot is not None:
            robot.robot.shutdown()

        rclpy.shutdown()


if __name__ == "__main__":
    main()