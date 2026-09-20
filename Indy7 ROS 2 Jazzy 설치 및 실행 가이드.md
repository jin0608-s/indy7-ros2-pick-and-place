# Indy7 ROS 2 Jazzy 설치 및 실행 가이드

Neuromeka의 **Indy7** 협동로봇을 Ubuntu 24.04 + ROS 2 Jazzy 환경에서 설치하고, RViz 모델 확인 → Gazebo 시뮬레이션 → MoveIt 2까지 실행하는 방법을 정리한 문서입니다.

---

## 1. 개발 환경

| 항목              | 버전              |
| --------------- | --------------- |
| OS              | Ubuntu 24.04    |
| ROS             | ROS 2 Jazzy     |
| Python          | Python 3.12     |
| Gazebo          | Gazebo Harmonic |
| Robot           | Neuromeka Indy7 |
| Middleware      | Cyclone DDS     |
| Motion Planning | MoveIt 2        |

---

# 2. Indy7 전용 Workspace 생성

기존 ROS 프로젝트와 분리하여 Indy7 전용 workspace를 생성합니다.

```bash
cd ~/temp

mkdir -p indy_ws/src

cd ~/temp/indy_ws/src
```

최종적인 workspace 구조는 다음과 같습니다.

```text
~/temp/indy_ws/
├── src/
│   └── indy-ros2/
├── build/
├── install/
├── log/
└── .venv/
```

---

# 3. Neuromeka Indy ROS 2 다운로드

Neuromeka의 `indy-ros2` 저장소에서 Jazzy용 브랜치를 clone합니다.

```bash
cd ~/temp/indy_ws/src

git clone -b jazzy-indyDCP3 https://github.com/neuromeka-robotics/indy-ros2.git
```

다운로드가 정상적으로 되었는지 확인합니다.

```bash
ls
```

다음과 같이 `indy-ros2` 디렉터리가 나타나면 정상입니다.

```text
indy-ros2
```

---

# 4. ROS 2 및 Indy7 관련 패키지 설치

## 4.1 기본 개발 패키지

```bash
sudo apt update

sudo apt install -y \
python3-colcon-common-extensions \
python3-rosdep \
python3-venv
```

## 4.2 ROS 2 Jazzy 패키지

Indy7의 description, Gazebo, ros2_control 및 MoveIt 2 실행에 필요한 패키지를 설치합니다.

```bash
sudo apt install -y \
ros-jazzy-ament-cmake \
ros-jazzy-xacro \
ros-jazzy-ros-base \
ros-jazzy-moveit \
ros-jazzy-moveit-servo \
ros-jazzy-moveit-visual-tools \
ros-jazzy-moveit-resources \
ros-jazzy-moveit-ros-move-group \
ros-jazzy-moveit-planners-ompl \
ros-jazzy-moveit-kinematics \
ros-jazzy-moveit-ros-perception \
ros-jazzy-ros2-control \
ros-jazzy-ros2-controllers \
ros-jazzy-controller-manager \
ros-jazzy-joint-state-broadcaster \
ros-jazzy-joint-state-publisher-gui \
ros-jazzy-joint-trajectory-controller \
ros-jazzy-rviz-visual-tools \
ros-jazzy-geometric-shapes \
ros-jazzy-gz-ros2-control \
ros-jazzy-ros-gz
```

---

# 5. Cyclone DDS 설정

ROS 2 통신을 위해 Cyclone DDS를 설치합니다.

```bash
sudo apt install -y ros-jazzy-rmw-cyclonedds-cpp
```

기본 RMW 구현을 Cyclone DDS로 설정합니다.

```bash
echo 'export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp' >> ~/.bashrc
```

설정을 적용합니다.

```bash
source ~/.bashrc
```

설정이 적용되었는지 확인할 수 있습니다.

```bash
echo $RMW_IMPLEMENTATION
```

정상적으로 설정되었다면:

```text
rmw_cyclonedds_cpp
```

가 출력됩니다.

---

# 6. Python 가상환경 설정

Indy ROS 2에서 사용하는 Python 패키지를 별도의 가상환경에서 관리합니다.

## 6.1 가상환경 생성

```bash
cd ~/temp/indy_ws

python3 -m venv .venv
```

## 6.2 가상환경 활성화

```bash
source .venv/bin/activate
```

터미널 앞에 다음과 같이 `(.venv)`가 표시되면 정상입니다.

```text
(.venv) user@ubuntu:~/temp/indy_ws$
```

## 6.3 Python 패키지 설치

먼저 pip를 업데이트합니다.

```bash
pip install --upgrade pip
```

필요한 패키지를 설치합니다.

```bash
pip install catkin_pkg empy lark-parser
```

추가 의존성도 설치합니다.

```bash
pip install pyyaml jinja2 typeguard neuromeka
```

---

# 7. rosdep 의존성 설치

먼저 ROS 2 Jazzy 환경을 불러옵니다.

```bash
source /opt/ros/jazzy/setup.bash
```

workspace로 이동합니다.

```bash
cd ~/temp/indy_ws
```

Indy ROS 2 패키지의 의존성을 설치합니다.

```bash
rosdep install --from-paths src --ignore-src -r -y
```

설치 과정에서 일부 패키지가 이미 설치되어 있다는 메시지가 나타날 수 있습니다.

---

# 8. Indy7 Workspace 빌드

workspace의 루트 디렉터리에서 빌드합니다.

```bash
cd ~/temp/indy_ws

colcon build
```

빌드가 완료되면 `build`, `install`, `log` 디렉터리가 생성됩니다.

```text
indy_ws/
├── src/
│   └── indy-ros2/
├── build/
├── install/
├── log/
└── .venv/
```

---

# 9. Workspace 적용

빌드한 Indy7 패키지를 현재 터미널에 적용합니다.

```bash
source ~/temp/indy_ws/install/setup.bash
```

Indy 관련 패키지가 정상적으로 등록되었는지 확인합니다.

```bash
ros2 pkg list | grep indy
```

여러 Indy 관련 패키지가 출력되면 정상적으로 빌드된 것입니다.

예:

```text
indy_description
indy_gazebo
indy_moveit
...
```

---

# 10. Indy7 모델 확인

가장 먼저 Gazebo를 실행하기 전에 **Indy7 모델 자체가 정상적으로 로드되는지 확인**합니다.

ROS 2 Jazzy 환경을 불러옵니다.

```bash
source /opt/ros/jazzy/setup.bash
```

Indy workspace를 적용합니다.

```bash
source ~/temp/indy_ws/install/setup.bash
```

Indy7 description을 실행합니다.

```bash
ros2 launch indy_description indy_display.launch.py indy_type:=indy7
```

정상적으로 실행되면 RViz에서 Indy7 로봇 모델을 확인할 수 있습니다.

### 확인 사항

* Indy7 모델이 정상적으로 표시되는지
* 각 관절이 정상적으로 연결되어 있는지
* 로봇의 링크가 깨지지 않았는지
* TF가 정상적으로 생성되는지

---

# 11. Gazebo에서 Indy7 실행

Indy7의 Gazebo 시뮬레이션을 실행합니다.

먼저 ROS 2 Jazzy 환경을 적용합니다.

```bash
source /opt/ros/jazzy/setup.bash
```

Indy workspace를 적용합니다.

```bash
source ~/temp/indy_ws/install/setup.bash
```

Python 가상환경을 활성화합니다.

```bash
source ~/temp/indy_ws/.venv/bin/activate
```

Gazebo를 실행합니다.

```bash
ros2 launch indy_gazebo indy_gazebo.launch.py indy_type:=indy7
```

정상적으로 실행되면 Gazebo에서 Indy7 로봇을 확인할 수 있습니다.

### 확인 사항

* Gazebo가 정상적으로 실행되는지
* Indy7 모델이 생성되는지
* 관절이 정상적으로 표시되는지
* ros2_control이 정상적으로 로드되는지
* Joint State가 정상적으로 전달되는지

---

# 12. MoveIt 2 실행

Gazebo에서 Indy7을 실행한 상태에서 MoveIt 2를 실행합니다.

```bash
ros2 launch indy_moveit indy_moveit_gazebo.launch.py indy_type:=indy7
```

정상적으로 실행되면 MoveIt 2와 Gazebo의 Indy7을 연동하여 사용할 수 있습니다.

MoveIt 2에서는 다음 기능을 확인할 수 있습니다.

* Robot Model
* Planning Group
* Joint State
* Motion Planning
* Trajectory Planning
* Gazebo Robot Control

---

# 13. 전체 실행 순서

처음부터 실행할 경우 다음 순서로 진행합니다.

### Terminal 1 — Indy7 Gazebo

```bash
source /opt/ros/jazzy/setup.bash
source ~/temp/indy_ws/install/setup.bash
source ~/temp/indy_ws/.venv/bin/activate

ros2 launch indy_gazebo indy_gazebo.launch.py indy_type:=indy7
```

### Terminal 2 — MoveIt 2

```bash
source /opt/ros/jazzy/setup.bash
source ~/temp/indy_ws/install/setup.bash
source ~/temp/indy_ws/.venv/bin/activate

ros2 launch indy_moveit indy_moveit_gazebo.launch.py indy_type:=indy7
```

---

# 14. 설치 확인

### ROS 2 버전 확인

```bash
ros2 --version
```

### Indy 패키지 확인

```bash
ros2 pkg list | grep indy
```

### RMW 확인

```bash
echo $RMW_IMPLEMENTATION
```

결과:

```text
rmw_cyclonedds_cpp
```

### Gazebo 확인

```bash
gz sim --version
```

### MoveIt 관련 패키지 확인

```bash
ros2 pkg list | grep moveit
```

---

# 15. GitHub에 업로드할 때

`.gitignore`에는 빌드 결과물과 Python 가상환경을 제외하는 것을 권장합니다.

```gitignore
# ROS 2
build/
install/
log/

# Python virtual environment
.venv/

# Python cache
__pycache__/
*.pyc

# VS Code
.vscode/

# ROS logs
*.log
```

Git 저장소에 올릴 때:

```bash
git add "Indy7 ROS 2 Jazzy 설치 및 실행 가이드.md"
git commit -m "docs: add Indy7 ROS2 Jazzy installation guide"
git push
```

---

# 16. 최종 구조

설치가 완료된 Indy7 workspace는 다음과 같은 구조를 갖습니다.

```text
~/temp/indy
│
├── src
│   └── indy-ros2
│       ├── indy_description
│       ├── indy_gazebo
│       ├── indy_moveit
│       └── ...
│
├── build
├── install
├── log
│
└── .venv
```

이 workspace를 기반으로 이후 **Indy7 + Gazebo + MoveIt 2를 이용한 로봇 제어 및 경로 계획 실습**을 진행할 수 있습니다.
