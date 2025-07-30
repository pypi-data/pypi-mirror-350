from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.platypus import Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.units import mm
from datetime import datetime
from scp import SCPClient
from PIL import Image as Img
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import paramiko
import json
import time
import csv
import os

# from neuromeka import IndyDCP3

print("here")

class PerformanceBenchmark:    
    def __init__(self, step_ip, robot_name, category, target_path):
        # 사전에 측정된 각 로봇의 기준 데이터
        self.benchmark = {
            'Indy7': {
                'joint_motion': {
                    'benchmark_pos': {
                        1: {'RMS Error': 0.0010679608197766508, 'Max Error': 0.0025580000000000602},
                        2: {'RMS Error': 0.0006629722840178017, 'Max Error': 0.0016890000000000516},
                        3: {'RMS Error': 0.00026698869878287885, 'Max Error': 0.0007610000000002337},
                        4: {'RMS Error': 0.0006332673190881512, 'Max Error': 0.002307000000000059},
                        5: {'RMS Error': 0.0003769276129520633, 'Max Error': 0.0016940000000000843},
                        6: {'RMS Error': 0.000660136536956631, 'Max Error': 0.0023360000000001158}
                    },
                    'benchmark_vel': {
                        1: {'RMS Error': 0.013590021537021813, 'Max Error': 0.06461700000000015},
                        2: {'RMS Error': 0.011511617374396885, 'Max Error': 0.05181400000000003},
                        3: {'RMS Error': 0.026357345475827937, 'Max Error': 0.14511800000000008},
                        4: {'RMS Error': 0.02682945597175326, 'Max Error': 0.12799000000000005},
                        5: {'RMS Error': 0.017096185025341885, 'Max Error': 0.07719600000000004},
                        6: {'RMS Error': 0.01043740251428306, 'Max Error': 0.040326}
                    },
                    'benchmark_torque': {1: {'Max torque': 239.343567, 'Min torque': -222.051718},
                                         2: {'Max torque': 179.071569, 'Min torque': -189.113692},
                                         3: {'Max torque': 86.857993, 'Min torque': -76.877952},
                                         4: {'Max torque': 24.14527, 'Min torque': -27.27053},
                                         5: {'Max torque': 14.354939, 'Min torque': -13.502547},
                                         6: {'Max torque': 21.698, 'Min torque': -21.260868}
                                         },
                    'joint_gain': {
                        'kp': [100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
                        'kv': [20.0, 20.0, 20.0, 20.0, 20.0, 20.0],
                        'kl2': [800.0, 800.0, 600.0, 400.0, 400.0, 400.0]
                    }
                },
                'task_motion': {
                    'benchmark_trans': [
                        ['X', 0.0001725565353294829, 0.0005269999999999997],
                        ['Y', 0.00036342131302670287, 0.0009500000000000029],
                        ['Z', 0.00028573317573190666, 0.0008619999999999739]
                    ],
                    'benchmark_rot': [
                        ['U', 0.0001897, 0.00035],
                        ['V', 0.0002958, 0.00078],
                        ['W', 0.0001931, 0.000483]
                    ],
                    'task_gain': {
                        'kp': [100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
                        'kv': [20.0, 20.0, 20.0, 20.0, 20.0, 20.0],
                        'kl2': [800.0, 800.0, 600.0, 400.0, 400.0, 400.0]
                    }
                },
                'movelf_motion': {
                    'benchmark_trans': [
                        ['X', 0.0001725565353294829, 0.0005269999999999997],
                        ['Y', 0.00036342131302670287, 0.0009500000000000029],
                        ['Z', 0.00028573317573190666, 0.0008619999999999739]
                    ],
                    'benchmark_rot': [
                        ['U', 0.0001897, 0.00035],
                        ['V', 0.0002958, 0.00078],
                        ['W', 0.0001931, 0.000483]
                    ],
                    'force_gain': {
                        'kp': [100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
                        'kv': [20.0, 20.0, 20.0, 20.0, 20.0, 20.0],
                        'kl2': [800.0, 800.0, 600.0, 400.0, 400.0, 400.0],
                        'mass': [1.0, 1.0, 1.0, 0.06, 0.06, 0.06],
                        'damping': [2000.0, 2000.0, 2000.0, 200, 200, 200],
                        'stiffness': [650.0, 650.0, 650.0, 80, 80, 80]
                    }
                },
            },
            'Opti5v2': {
                'joint_motion': {
                    'benchmark_pos': {
                        1: {'RMS Error': 0.0010679608197766508, 'Max Error': 0.0025580000000000602},
                        2: {'RMS Error': 0.0006629722840178017, 'Max Error': 0.0016890000000000516},
                        3: {'RMS Error': 0.00026698869878287885, 'Max Error': 0.0007610000000002337},
                        4: {'RMS Error': 0.0006332673190881512, 'Max Error': 0.002307000000000059},
                        5: {'RMS Error': 0.0003769276129520633, 'Max Error': 0.0016940000000000843},
                        6: {'RMS Error': 0.000660136536956631, 'Max Error': 0.0023360000000001158}
                    },
                    'benchmark_vel': {
                        1: {'RMS Error': 0.013590021537021813, 'Max Error': 0.06461700000000015},
                        2: {'RMS Error': 0.011511617374396885, 'Max Error': 0.05181400000000003},
                        3: {'RMS Error': 0.026357345475827937, 'Max Error': 0.14511800000000008},
                        4: {'RMS Error': 0.02682945597175326, 'Max Error': 0.12799000000000005},
                        5: {'RMS Error': 0.017096185025341885, 'Max Error': 0.07719600000000004},
                        6: {'RMS Error': 0.01043740251428306, 'Max Error': 0.040326}
                    },
                    'benchmark_torque': {1: {'Max torque': 239.343567, 'Min torque': -222.051718},
                                         2: {'Max torque': 179.071569, 'Min torque': -189.113692},
                                         3: {'Max torque': 86.857993, 'Min torque': -76.877952},
                                         4: {'Max torque': 24.14527, 'Min torque': -27.27053},
                                         5: {'Max torque': 14.354939, 'Min torque': -13.502547},
                                         6: {'Max torque': 21.698, 'Min torque': -21.260868}
                                         },
                    'joint_gain': {
                        'kp': [100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
                        'kv': [20.0, 20.0, 20.0, 20.0, 20.0, 20.0],
                        'kl2': [800.0, 800.0, 600.0, 400.0, 400.0, 400.0]
                    }
                },
                'task_motion': {
                    'benchmark_trans': [
                        ['X', 0.0001725565353294829, 0.0005269999999999997],
                        ['Y', 0.00036342131302670287, 0.0009500000000000029],
                        ['Z', 0.00028573317573190666, 0.0008619999999999739]
                    ],
                    'benchmark_rot': [
                        ['U', 0.0001897, 0.00035],
                        ['V', 0.0002958, 0.00078],
                        ['W', 0.0001931, 0.000483]
                    ],
                    'task_gain': {
                        'kp': [100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
                        'kv': [20.0, 20.0, 20.0, 20.0, 20.0, 20.0],
                        'kl2': [800.0, 800.0, 600.0, 400.0, 400.0, 400.0]
                    }
                },
                'movelf_motion': {
                    'benchmark_trans': [
                        ['X', 0.0001725565353294829, 0.0005269999999999997],
                        ['Y', 0.00036342131302670287, 0.0009500000000000029],
                        ['Z', 0.00028573317573190666, 0.0008619999999999739]
                    ],
                    'benchmark_rot': [
                        ['U', 0.0001897, 0.00035],
                        ['V', 0.0002958, 0.00078],
                        ['W', 0.0001931, 0.000483]
                    ],
                    'force_gain': {
                        'kp': [100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
                        'kv': [20.0, 20.0, 20.0, 20.0, 20.0, 20.0],
                        'kl2': [800.0, 800.0, 600.0, 400.0, 400.0, 400.0],
                        'mass': [1.0, 1.0, 1.0, 0.06, 0.06, 0.06],
                        'damping': [2000.0, 2000.0, 2000.0, 200, 200, 200],
                        'stiffness': [650.0, 650.0, 650.0, 80, 80, 80]
                    }
                },
            },
            'Indy7v2': {
                'task_motion': {
                    'benchmark_trans': [
                        ['X', 0.0001725565353294829, 0.0005269999999999997],
                        ['Y', 0.00036342131302670287, 0.0009500000000000029],
                        ['Z', 0.00028573317573190666, 0.0008619999999999739]
                    ],
                    'benchmark_rot': [
                        ['U', 1.8411358678934133, 3.141852],
                        ['V', 1.8327148841966145, 3.139553],
                        ['W', 1.8406441602857722, 3.141572]
                    ],
                    'task_gain': {
                        'kp': [100.0, 100.0, 160.0, 160.0, 160.0, 160.0],
                        'kv': [20.0, 20.0, 26.0, 26.0, 26.0, 26.0],
                        'kl2': [650.0, 650.0, 350.0, 70.0, 70.0, 70.0]
                    }
                },
                'joint_motion': {
                    'benchmark_pos': {
                        1: {'RMS Error': 0.0010679608197766508, 'Max Error': 0.0025580000000000602},
                        2: {'RMS Error': 0.0006629722840178017, 'Max Error': 0.0016890000000000516},
                        3: {'RMS Error': 0.00026698869878287885, 'Max Error': 0.0007610000000002337},
                        4: {'RMS Error': 0.0006332673190881512, 'Max Error': 0.002307000000000059},
                        5: {'RMS Error': 0.0003769276129520633, 'Max Error': 0.0016940000000000843},
                        6: {'RMS Error': 0.000660136536956631, 'Max Error': 0.0023360000000001158}
                    },
                    'benchmark_vel': {
                        1: {'RMS Error': 0.013590021537021813, 'Max Error': 0.06461700000000015},
                        2: {'RMS Error': 0.011511617374396885, 'Max Error': 0.05181400000000003},
                        3: {'RMS Error': 0.026357345475827937, 'Max Error': 0.14511800000000008},
                        4: {'RMS Error': 0.02682945597175326, 'Max Error': 0.12799000000000005},
                        5: {'RMS Error': 0.017096185025341885, 'Max Error': 0.07719600000000004},
                        6: {'RMS Error': 0.01043740251428306, 'Max Error': 0.040326}
                    },
                    'benchmark_torque': {1: {'Max torque': 239.343567, 'Min torque': -222.051718},
                                         2: {'Max torque': 179.071569, 'Min torque': -189.113692},
                                         3: {'Max torque': 86.857993, 'Min torque': -76.877952},
                                         4: {'Max torque': 24.14527, 'Min torque': -27.27053},
                                         5: {'Max torque': 14.354939, 'Min torque': -13.502547},
                                         6: {'Max torque': 21.698, 'Min torque': -21.260868}
                                         },
                    'joint_gain': {
                        'kp': [100.0, 100.0, 160.0, 160.0, 160.0, 160.0],
                        'kv': [20.0, 20.0, 26.0, 26.0, 26.0, 26.0],
                        'kl2': [650.0, 650.0, 350.0, 70.0, 70.0, 70.0]
                    }
                }
            },
            'Indy12v1': {
                'task_motion': {
                    'benchmark_trans': [
                        ['X', 0.0001725565353294829, 0.0005269999999999997],
                        ['Y', 0.00036342131302670287, 0.0009500000000000029],
                        ['Z', 0.00028573317573190666, 0.0008619999999999739]
                    ],
                    'benchmark_rot': [
                        ['U', 1.8411358678934133, 3.141852],
                        ['V', 1.8327148841966145, 3.139553],
                        ['W', 1.8406441602857722, 3.141572]
                    ],
                    'task_gain': {
                        'kp': [180.0, 180.0, 120.0, 100.0, 100.0, 100.0],
                        'kv': [25.0, 25.0, 22.0, 22.0, 20.0, 20.0],
                        'kl2': [1200.0, 1200.0, 900.0, 600.0, 600.0, 600.0]
                    }
                },
                'joint_motion': {
                    'benchmark_pos': {
                        1: {'RMS Error': 0.0010679608197766508, 'Max Error': 0.0025580000000000602},
                        2: {'RMS Error': 0.0006629722840178017, 'Max Error': 0.0016890000000000516},
                        3: {'RMS Error': 0.00026698869878287885, 'Max Error': 0.0007610000000002337},
                        4: {'RMS Error': 0.0006332673190881512, 'Max Error': 0.002307000000000059},
                        5: {'RMS Error': 0.0003769276129520633, 'Max Error': 0.0016940000000000843},
                        6: {'RMS Error': 0.000660136536956631, 'Max Error': 0.0023360000000001158}
                    },
                    'benchmark_vel': {
                        1: {'RMS Error': 0.013590021537021813, 'Max Error': 0.06461700000000015},
                        2: {'RMS Error': 0.011511617374396885, 'Max Error': 0.05181400000000003},
                        3: {'RMS Error': 0.026357345475827937, 'Max Error': 0.14511800000000008},
                        4: {'RMS Error': 0.02682945597175326, 'Max Error': 0.12799000000000005},
                        5: {'RMS Error': 0.017096185025341885, 'Max Error': 0.07719600000000004},
                        6: {'RMS Error': 0.01043740251428306, 'Max Error': 0.040326}
                    },
                    'benchmark_torque': {
                        1: {'Max torque': 239.343567, 'Min torque': -222.051718},
                        2: {'Max torque': 179.071569, 'Min torque': -189.113692},
                        3: {'Max torque': 86.857993, 'Min torque': -76.877952},
                        4: {'Max torque': 24.14527, 'Min torque': -27.27053},
                        5: {'Max torque': 14.354939, 'Min torque': -13.502547},
                        6: {'Max torque': 21.698, 'Min torque': -21.260868}
                    },
                    'joint_gain': {
                        'kp': [180.0, 180.0, 120.0, 100.0, 100.0, 100.0],
                        'kv': [25.0, 25.0, 22.0, 22.0, 20.0, 20.0],
                        'kl2': [1200.0, 1200.0, 900.0, 600.0, 600.0, 600.0]
                    }
                }
            },
            'Indy12v2': {
                'task_motion': {
                    'benchmark_trans': [
                        ['X', 0.0001725565353294829, 0.0005269999999999997],
                        ['Y', 0.00036342131302670287, 0.0009500000000000029],
                        ['Z', 0.00028573317573190666, 0.0008619999999999739]
                    ],
                    'benchmark_rot': [
                        ['U', 1.8411358678934133, 3.141852],
                        ['V', 1.8327148841966145, 3.139553],
                        ['W', 1.8406441602857722, 3.141572]
                    ],
                    'task_gain': {
                        'kp': [180.0, 180.0, 120.0, 100.0, 100.0, 100.0],
                        'kv': [25.0, 25.0, 22.0, 22.0, 20.0, 20.0],
                        'kl2': [1200.0, 1200.0, 900.0, 600.0, 600.0, 600.0]
                    }
                },
                'joint_motion': {
                    'benchmark_pos': {
                        1: {'RMS Error': 0.0010679608197766508, 'Max Error': 0.0025580000000000602},
                        2: {'RMS Error': 0.0006629722840178017, 'Max Error': 0.0016890000000000516},
                        3: {'RMS Error': 0.00026698869878287885, 'Max Error': 0.0007610000000002337},
                        4: {'RMS Error': 0.0006332673190881512, 'Max Error': 0.002307000000000059},
                        5: {'RMS Error': 0.0003769276129520633, 'Max Error': 0.0016940000000000843},
                        6: {'RMS Error': 0.000660136536956631, 'Max Error': 0.0023360000000001158}
                    },
                    'benchmark_vel': {
                        1: {'RMS Error': 0.013590021537021813, 'Max Error': 0.06461700000000015},
                        2: {'RMS Error': 0.011511617374396885, 'Max Error': 0.05181400000000003},
                        3: {'RMS Error': 0.026357345475827937, 'Max Error': 0.14511800000000008},
                        4: {'RMS Error': 0.02682945597175326, 'Max Error': 0.12799000000000005},
                        5: {'RMS Error': 0.017096185025341885, 'Max Error': 0.07719600000000004},
                        6: {'RMS Error': 0.01043740251428306, 'Max Error': 0.040326}
                    },
                    'benchmark_torque': {
                        1: {'Max torque': 239.343567, 'Min torque': -222.051718},
                        2: {'Max torque': 179.071569, 'Min torque': -189.113692},
                        3: {'Max torque': 86.857993, 'Min torque': -76.877952},
                        4: {'Max torque': 24.14527, 'Min torque': -27.27053},
                        5: {'Max torque': 14.354939, 'Min torque': -13.502547},
                        6: {'Max torque': 21.698, 'Min torque': -21.260868}
                    },
                    'joint_gain': {
                        'kp': [180.0, 180.0, 120.0, 100.0, 100.0, 100.0],
                        'kv': [25.0, 25.0, 22.0, 22.0, 20.0, 20.0],
                        'kl2': [1200.0, 1200.0, 900.0, 600.0, 600.0, 600.0]
                    }
                }
            },
        }

        # Check if the robot name and category exist
        if robot_name in self.benchmark and category in self.benchmark[robot_name]:
            self.benchmark_critia = self.benchmark[robot_name][category]
        else:
            pass

        # RTRecord.csv에서 불러온 데이터가 저장될 변수
        self.record = {
            "t": [], "cycle_time": [], "period": [],
            **{f"q{i}": [] for i in range(1, 7)},
            **{f"qdot{i}": [] for i in range(1, 7)},
            **{f"qddot{i}": [] for i in range(1, 7)},
            **{f"tau{i}": [] for i in range(1, 7)},
            **{f"tauact{i}": [] for i in range(1, 7)},
            **{f"qd{i}": [] for i in range(1, 7)},
            **{f"qdotd{i}": [] for i in range(1, 7)},
            **{f"qddotd{i}": [] for i in range(1, 7)},
            **{f"p{i}": [] for i in range(1, 7)},
            **{f"pd{i}": [] for i in range(1, 7)},
            **{f"qe{i}": [] for i in range(1, 7)},
            **{f"qdote{i}": [] for i in range(1, 7)},
            **{f"pe{i}": [] for i in range(1, 7)},
            **{f"fe{i}": [] for i in range(1, 7)},
            **{f"fdes{i}": [] for i in range(1, 7)},
            **{f"fact{i}": [] for i in range(1, 7)},
            **{f"tauidyn{i}": [] for i in range(1, 7)},
            **{f"tauref{i}": [] for i in range(1, 7)},
            **{f"taugrav{i}": [] for i in range(1, 7)},
            **{f"taufric{i}": [] for i in range(1, 7)},
            **{f"tauext{i}": [] for i in range(1, 7)},
            **{f"tauJts{i}": [] for i in range(1, 7)},
            **{f"tauJtsRaw1{i}": [] for i in range(1, 7)},
            **{f"tauJtsRaw2{i}": [] for i in range(1, 7)},
        }

        self.step_ip = step_ip
        self.robot_name = robot_name
        self.category = category

        # RTRecord.csv 파일이 있는 경로
        self.file_path = '/home/user/release/IndyDeployment/RTLog'
        self.file_name = 'RTRecord.csv'

        # result_path가 생성될 경로 설정
        self.target_path = target_path

        # 결과 Plot과 PDF가 저장될 경로
        self.result_path = ''

    def run_program(self):
        def is_file_stable(sftp, remote_file_path, stability_time=15):
            """
            원격 파일이 안정적인지 확인하는 함수.

            :param sftp: SFTP 클라이언트 객체
            :param remote_file_path: 원격 파일 경로
            :param stability_time: 파일 크기가 안정적으로 유지되어야 하는 시간(초)
            :return: 파일이 안정적이면 True, 그렇지 않으면 False
            """
            initial_size = sftp.stat(remote_file_path).st_size
            time.sleep(stability_time)
            final_size = sftp.stat(remote_file_path).st_size

            return initial_size == final_size

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.step_ip, username='root', password='root')

        sftp = ssh.open_sftp()

        deploy_file = '/home/user/release/IndyDeployment/indyDeploy.json'

        with sftp.open(deploy_file, 'r') as file:
            data = json.load(file)
            deploy_data = dict(data)

        if deploy_data['RTTasks']['RecordingTask']['Enabled'] == 0:
            deploy_data['RTTasks']['RecordingTask']['Enabled'] = 1

            with sftp.open(deploy_file, 'w') as file:
                json.dump(deploy_data, file, ensure_ascii=False, indent=4)

            print("RecordingTask is disabled. Please restart the STEP.")
        else:
            cur_path = '/home/user/release/IndyDeployment/'
            prog_name = f'{self.category}.{self.robot_name.lower()}.json'
            # prog_path = cur_path + '/' + 'motion' + '/' + prog_name

            indy = IndyDCP3(self.step_ip)
            indy.play_program(prog_name=prog_name)

            time.sleep(3)

            while indy.get_control_data()['op_state'] == 6:
                time.sleep(2)

            csv_file = '/home/user/release/IndyDeployment/RTLog/RTRecord.csv'

            while is_file_stable(sftp, csv_file):
                print('Waiting for saving RTRecord.csv....')
            print('RTRecord.csv is saved!!!')

    def addPageNumber(self, canvas, doc):
        """
        Add the page number 215.9 X 279.4
        """
        page_num = canvas.getPageNumber()
        text = "-%s-" % page_num
        canvas.drawCentredString(105 * mm, 20 * mm, text)

    # Generate result path for save plot and result PDF
    def generate_result_path(self):
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        self.result_path = os.path.join(self.target_path, self.category, formatted_time)

        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)

    # Load RTRecord.csv on STEP(paramiko) & PC(local)
    def load_data_6dof_step(self):
        self.generate_result_path()

        csv_file = self.file_path + '/' + self.file_name
        result_csv_file = os.path.join(self.result_path, self.file_name)

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.step_ip, username='root', password='root')

        with SCPClient(ssh.get_transport()) as scp:
            scp.get(csv_file, result_csv_file)

        print(f"{self.file_name} downloaded successfully to {self.result_path}")

        # open the RTRecord.csv using `sftp`
        csv_file = open(result_csv_file)

        # read the contents of the file using `csv` library
        reader = csv.reader(csv_file, delimiter=",")

        for line in reader:
            self.record["t"].append(float(line[0]))

            for i in range(1, 7):
                self.record[f"q{i}"].append(np.rad2deg(float(line[2 + i])))
                self.record[f"qdot{i}"].append(np.rad2deg(float(line[8 + i])))
                self.record[f"tau{i}"].append(float(line[20 + i]))
                self.record[f"tauact{i}"].append(float(line[26 + i]))
                self.record[f"qd{i}"].append(np.rad2deg(float(line[32 + i])))
                self.record[f"qdotd{i}"].append(np.rad2deg(float(line[38 + i])))
                self.record[f"p{i}"].append(float(line[50 + i]))
                self.record[f"pd{i}"].append(float(line[56 + i]))
                self.record[f"fact{i}"].append(float(line[62 + i]))
                self.record[f"fdes{i}"].append(-float(line[68 + i]))
                self.record[f"tauref{i}"].append(float(line[80 + i]))
                self.record[f"taugrav{i}"].append(float(line[86 + i]))
                self.record[f"taufric{i}"].append(float(line[92 + i]))
                self.record[f"tauJts{i}"].append(float(line[104 + i]))
                self.record[f"pe{i}"].append(float(line[122 + i]))
                # Compute Joint and Task Position errors
                self.record[f"qe{i}"].append(self.record[f"qd{i}"][-1] - self.record[f"q{i}"][-1])
                self.record[f"qdote{i}"].append(self.record[f"qdotd{i}"][-1] - self.record[f"qdot{i}"][-1])
                # self.record[f"pe{i}"].append(self.record[f"pd{i}"][-1] - self.record[f"p{i}"][-1])

    # Plot recorded data
    def extract_errors_for_all_joints(self, num_joints=6):
        errors = {}
        for joint_number in range(1, num_joints + 1):
            rms_error, max_error = self.plot_error_position_plt(joint_number)
            errors[joint_number] = {'RMS Error': rms_error, 'Max Error': max_error}
        return errors

    def extract_vel_errors_for_all_joints(self, num_joints=6):
        errors = {}
        for joint_number in range(1, num_joints + 1):
            rms_error, max_error = self.plot_error_velocity_plt(joint_number)
            errors[joint_number] = {'RMS Error': rms_error, 'Max Error': max_error}
        return errors

    def extract_torque_all_joints(self, num_joints=6):
        torques = {}
        for joint_number in range(1, num_joints + 1):
            min_torque, max_torque = self.plot_torque_report_plt(joint_number)
            torques[joint_number] = {'Max torque': max_torque, 'Min torque': min_torque}
        return torques

    def extract_errors_translation_rotation(self, num_joints=6):
        translation_labels = {1: 'X', 2: 'Y', 3: 'Z'}
        rotation_labels = {4: 'U', 5: 'V', 6: 'W'}
        translation_errors = []
        rotation_errors = []

        for joint_number in range(1, num_joints + 1):
            rms_error, max_error = self.plot_error_task_translation_rotation_plt(joint_number)

            if joint_number <= 3:  # translation (X, Y, Z)
                label = translation_labels[joint_number]
                translation_errors.append([label, rms_error, max_error])
            else:  # Rotation (U, V, W)
                label = rotation_labels[joint_number]
                rotation_errors.append([label, rms_error, max_error])

        return translation_errors, rotation_errors

    def plot_position_plt(self, joint_number):
        pos_actual = np.array(self.record['q' + str(joint_number)])
        pos_desired = np.array(self.record['qd' + str(joint_number)])
        max_pos, min_pos = np.max(pos_actual), np.min(pos_actual)

        x = self.record['t']
        y1 = pos_actual
        y2 = pos_desired

        plt.suptitle(f'Joint {joint_number} Position')
        plt.title(f'(Min: {min_pos:.3f} deg, Max: {max_pos:.3f} deg)')
        plt.xlabel('Time (s)')
        plt.ylabel('Position (deg)')
        plt.grid(axis='both', linestyle='--', linewidth=1, color='lightgray')
        plt.plot(x, y1, linestyle='solid', linewidth=2, color='b')
        plt.plot(x, y2, linestyle='--', linewidth=2, color='red')
        plt.tight_layout()
        file_name = f'Joint_{joint_number}_Position.png'
        full_path = os.path.join(self.result_path, file_name)

        plt.savefig(full_path)
        plt.cla()

    def plot_error_position_plt(self, joint_number):
        errors = np.array(self.record['qe' + str(joint_number)])
        rms_error = np.sqrt(np.mean(errors ** 2))
        max_error = np.max(np.abs(errors))

        x = self.record['t']
        y = errors

        plt.suptitle(f'Joint {joint_number} Position Tracking Error')
        plt.title(f'(RMS Error: {rms_error:.3f} deg, Max Error: {max_error:.3f} deg)')
        plt.xlabel('Time (s)')
        plt.ylabel('Error (deg)')
        plt.grid(axis='both', linestyle='--', linewidth=1, color='lightgray')
        plt.plot(x, y, linestyle='solid', linewidth=1, color='b')
        plt.tight_layout()
        file_name = f'Joint_{joint_number}_Pose_Tracking_Error.png'
        full_path = os.path.join(self.result_path, file_name)

        plt.savefig(full_path)
        plt.cla()
        return rms_error, max_error

    # Generate Joint motion benchmark PDF
    def plot_velocity_plt(self, joint_number):
        vel_actual = np.array(self.record['qdot' + str(joint_number)])
        vel_desired = np.array(self.record['qdotd' + str(joint_number)])
        max_vel, min_vel = np.max(vel_actual), np.min(vel_actual)

        x = self.record['t']
        y1 = vel_actual
        y2 = vel_desired

        plt.suptitle(f'Joint {joint_number} Velocity')
        plt.title(f'(Min: {min_vel:.3f} deg/s, Max: {max_vel:.3f} deg/s)')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity (deg/s)')
        plt.grid(axis='both', linestyle='--', linewidth=1, color='lightgray')
        plt.plot(x, y1, linestyle='solid', linewidth=2, color='b')
        plt.plot(x, y2, linestyle='--', linewidth=2, color='red')
        plt.tight_layout()
        file_name = f'Joint_{joint_number}_Velocity.png'
        full_path = os.path.join(self.result_path, file_name)

        plt.savefig(full_path)
        plt.cla()

    def plot_error_velocity_plt(self, joint_number):
        errors = np.array(self.record['qdote' + str(joint_number)])
        rms_error = np.sqrt(np.mean(errors ** 2))
        max_error = np.max(np.abs(errors))

        x = self.record['t']
        y = errors

        plt.suptitle(f'Joint {joint_number} Velocity Tracking Error')
        plt.title(f'(RMS Error: {rms_error:.3f} deg/s, Max Error: {max_error:.3f} deg/s)')
        plt.xlabel('Time (s)')
        plt.ylabel('Error (deg/s)')
        plt.grid(axis='both', linestyle='--', linewidth=1, color='lightgray')
        plt.plot(x, y, linestyle='solid', linewidth=1, color='b')
        plt.tight_layout()
        file_name = f'Joint_{joint_number}_Vel_Tracking_Error.png'
        full_path = os.path.join(self.result_path, file_name)

        plt.savefig(full_path)
        plt.cla()
        return rms_error, max_error

    def plot_force_plt(self, joint_number):
        f_act = np.array(self.record['fact' + str(joint_number)])
        f_des = np.array(self.record['fdes' + str(joint_number)])
        max_f, min_f = np.max(f_act), np.min(f_act)

        x = self.record['t']
        y1 = f_act
        y2 = f_des

        plt.suptitle(f'Joint {joint_number} Force')
        plt.title(f'(Min: {min_f:.6f} Nm, Max: {max_f:.6f} Nm)')
        plt.xlabel('Time (s)')
        plt.ylabel('Force (Nm)')
        plt.grid(axis='both', linestyle='--', linewidth=1, color='lightgray')
        plt.plot(x, y1, linestyle='solid', linewidth=2, color='b')
        plt.plot(x, y2, linestyle='--', linewidth=2, color='red')
        plt.tight_layout()
        file_name = f'Joint_{joint_number}_Force.png'
        full_path = os.path.join(self.result_path, file_name)

        plt.savefig(full_path)
        plt.cla()

    def plot_friction_plt(self, joint_number):
        fric = np.array(self.record['taufric' + str(joint_number)])
        max_fric, min_fric = np.max(fric), np.min(fric)

        x = self.record['t']
        y = fric

        plt.suptitle(f'Joint {joint_number} Friction')
        plt.title(f'(Min: {min_fric:.6f} Nm, Max: {max_fric:.6f} Nm)')
        plt.xlabel('Time (s)')
        plt.ylabel('Friction (Nm)')
        plt.grid(axis='both', linestyle='--', linewidth=1, color='lightgray')
        plt.plot(x, y, linestyle='solid', linewidth=2, color='b')
        plt.tight_layout()
        file_name = f'Joint_{joint_number}_Friction.png'
        full_path = os.path.join(self.result_path, file_name)

        plt.savefig(full_path)
        plt.cla()

    def plot_torque_report_plt(self, joint_number):
        torque = np.array(self.record['tau' + str(joint_number)])
        min_torque, max_torque = np.min(torque), np.max(torque)

        x = self.record['t']
        y = torque

        plt.suptitle(f'Joint {joint_number} Torque')
        plt.title(f'(Max torque: {max_torque:.4f} Nm, Min torque: {min_torque:.4f} Nm)')
        plt.xlabel('Time (s)')
        plt.ylabel('Joint torque (Nm)')
        plt.grid(axis='both', linestyle='--', linewidth=1, color='lightgray')
        plt.plot(x, y, linestyle='solid', linewidth=1, color='b')
        plt.tight_layout()
        file_name = f'Joint_{joint_number}_Torque.png'
        full_path = os.path.join(self.result_path, file_name)

        plt.savefig(full_path)
        plt.cla()
        return min_torque, max_torque

    def plot_error_task_translation_rotation_plt(self, joint_number):
        labels = {1: 'X', 2: 'Y', 3: 'Z', 4: 'U', 5: 'V', 6: 'W'}

        label = labels[joint_number]

        if joint_number in [1, 2, 3]:
            errors = np.array(self.record['pe' + str(joint_number)])
            errors = errors * 1000
            rms_error = np.sqrt(np.mean(errors ** 2))
            max_error = np.max(np.abs(errors))
            error_type = 'Translation'
            y_axis = 'mm'
        elif joint_number in [4, 5, 6]:
            errors = np.array(self.record['pe' + str(joint_number)])
            errors = np.rad2deg(errors)
            rms_error = np.sqrt(np.mean(errors ** 2))
            max_error = np.max(np.abs(errors))
            error_type = 'Rotation'
            y_axis = 'deg'
        else:
            raise ValueError("Invalid joint number")

        x = self.record['t']
        y = errors

        plt.suptitle(f'{label} {error_type.capitalize()} Error')
        plt.title(f'(RMS Error: {rms_error:.6f} {y_axis}, Max Error: {max_error:.6f} {y_axis})')
        plt.xlabel('Time (s)')
        plt.ylabel(f'Error {y_axis}')
        plt.grid(axis='both', linestyle='--', linewidth=1, color='lightgray')
        plt.plot(x, y, linestyle='solid', linewidth=1, color='b')
        plt.tight_layout()

        file_name = f'{label}_{error_type.capitalize()}_Error.png'
        full_path = os.path.join(self.result_path, file_name)

        plt.savefig(full_path)
        plt.cla()
        plt.suptitle('')

        return rms_error, max_error

    def plot_task_motion_2D_plt(self, plot_axis):
        def extend_range(min_val, max_val, extension=0.008):
            return [min_val - extension, max_val + extension]

        if plot_axis == "XY":
            x1, x2 = self.record['pd1'], self.record['p1']
            y1, y2 = self.record['pd2'], self.record['p2']
            x_range = extend_range(min(self.record['p1'] + self.record['pd1']),
                                   max(self.record['p1'] + self.record['pd1']))
            y_range = extend_range(min(self.record['p2'] + self.record['pd2']),
                                   max(self.record['p2'] + self.record['pd2']))
            xtitle = "X-axis (m)"
            ytitle = "Y-axis (m)"
        elif plot_axis == "YZ":
            x1, x2 = self.record['pd2'], self.record['p2']
            y1, y2 = self.record['pd3'], self.record['p3']
            x_range = extend_range(min(self.record['p2'] + self.record['pd2']),
                                   max(self.record['p2'] + self.record['pd2']))
            y_range = extend_range(min(self.record['p3'] + self.record['pd3']),
                                   max(self.record['p3'] + self.record['pd3']))
            xtitle = "Y-axis (m)"
            ytitle = "Z-axis (m)"
        elif plot_axis == "XZ":
            x1, x2 = self.record['pd1'], self.record['p1']
            y1, y2 = self.record['pd3'], self.record['p3']
            x_range = extend_range(min(self.record['p1'] + self.record['pd1']),
                                   max(self.record['p1'] + self.record['pd1']))
            y_range = extend_range(min(self.record['p3'] + self.record['pd3']),
                                   max(self.record['p3'] + self.record['pd3']))
            xtitle = "X-axis (m)"
            ytitle = "Z-axis (m)"

        plt.suptitle(f'{plot_axis} Task Space Tracking')
        plt.xlabel(xtitle)
        plt.ylabel(ytitle)
        plt.xlim(x_range)
        plt.ylim(y_range)
        plt.grid(axis='both', linestyle='--', linewidth=1, color='lightgray')
        plt.plot(x1, y1, linestyle='solid', linewidth=1, color='black')
        plt.plot(x2, y2, linestyle='--', linewidth=1, color='red')
        plt.tight_layout()

        file_name = f'Task Space Tracking {plot_axis}.png'
        full_path = os.path.join(self.result_path, file_name)

        plt.savefig(full_path)
        plt.cla()

    def plot_task_motion_3D_plt(self):
        def extend_range(min_val, max_val, extension=0.01):
            return [min_val - extension, max_val + extension]

        x1, x2 = self.record['pd1'], self.record['p1']
        y1, y2 = self.record['pd2'], self.record['p2']
        z1, z2 = self.record['pd3'], self.record['p3']

        x_range = extend_range(min(self.record['p1'] + self.record['pd1']), max(self.record['p1'] + self.record['pd1']))
        y_range = extend_range(min(self.record['p2'] + self.record['pd2']), max(self.record['p2'] + self.record['pd2']))
        z_range = extend_range(min(self.record['p3'] + self.record['pd3']), max(self.record['p3'] + self.record['pd3']))

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        ax.set_title("Task Space Tracking 3D")
        ax.set_xlabel("X-axis (m)")
        ax.set_ylabel("Y-axis (m)")
        ax.set_zlabel("Z-axis (m)")
        ax.set_xlim(x_range)
        ax.set_ylim(y_range)
        ax.set_zlim(z_range)
        ax.plot(x1, y1, z1, linewidth=2, linestyle="solid", color="black")
        ax.plot(x2, y2, z2, linewidth=2, linestyle="--", color="red")

        file_name = 'Task Space Tracking 3D.png'
        full_path = os.path.join(self.result_path, file_name)

        plt.savefig(full_path)
        plt.cla()

    # Compare recorded data with benchmark
    def status_joint_error(self, combine_error):
        tolerance_pos, tolerance_vel = 0.05, 0.1
        status_list = [[3 for col in range(9)] for row in range(8)]
        error_list = [[3 for col in range(9)] for row in range(8)]

        for i in range(1, 7):
            target_rms_pos = float(combine_error.iloc[i, 1]) + float(combine_error.iloc[i, 1]) * tolerance_pos
            target_max_pos = float(combine_error.iloc[i, 2]) + float(combine_error.iloc[i, 2]) * tolerance_pos
            target_rms_vel = float(combine_error.iloc[i, 5]) + float(combine_error.iloc[i, 5]) * tolerance_vel
            target_max_vel = float(combine_error.iloc[i, 6]) + float(combine_error.iloc[i, 6]) * tolerance_vel
            test_rms_pos, test_max_pos = float(combine_error.iloc[i, 3]), float(combine_error.iloc[i, 4])
            test_rms_vel, test_max_vel = float(combine_error.iloc[i, 7]), float(combine_error.iloc[i, 8])

            if test_rms_pos <= target_rms_pos:
                status_list[i + 1][3] = 0
            else:
                status_list[i + 1][3] = 1
                error_list[i + 1][3] = (
                        ((test_rms_pos - float(combine_error.iloc[i, 1])) / float(combine_error.iloc[i, 1])) * 100)
            if test_max_pos <= target_max_pos:
                status_list[i + 1][4] = 0
            else:
                status_list[i + 1][4] = 1
                error_list[i + 1][4] = ((test_max_pos - float(combine_error.iloc[i, 2])) / float(
                    combine_error.iloc[i, 2])) * 100

            if test_rms_vel <= target_rms_vel:
                status_list[i + 1][7] = 0
            else:
                status_list[i + 1][7] = 1
                error_list[i + 1][7] = ((test_rms_vel - float(combine_error.iloc[i, 5])) / float(
                    combine_error.iloc[i, 5])) * 100
            if test_max_vel <= target_max_vel:
                status_list[i + 1][8] = 0
            else:
                status_list[i + 1][8] = 1
                error_list[i + 1][8] = ((test_max_vel - float(combine_error.iloc[i, 6])) / float(
                    combine_error.iloc[i, 6])) * 100

        return status_list, error_list

    def status_torque(self, combine_torque):
        tolerance_torque = 0.1

        status_torque_list = [[3 for col in range(11)] for row in range(8)]
        error_list = [[3 for col in range(11)] for row in range(8)]

        for i in range(1, 7):
            target_max_torque = float(combine_torque.iloc[i, 1]) + float(
                combine_torque.iloc[i, 1]) * tolerance_torque
            target_min_torque = float(combine_torque.iloc[i, 2]) + float(
                combine_torque.iloc[i, 2]) * tolerance_torque
            test_max_torque, test_min_torque = float(combine_torque.iloc[i, 3]), float(
                combine_torque.iloc[i, 4])

            if test_max_torque <= target_max_torque:
                status_torque_list[i + 1][3] = 0
            else:
                status_torque_list[i + 1][3] = 1
                error_list[i + 1][3] = ((test_max_torque - float(combine_torque.iloc[i, 1])) / float(
                    combine_torque.iloc[i, 1])) * 100
            if test_min_torque >= target_min_torque:
                status_torque_list[i + 1][4] = 0
            else:
                status_torque_list[i + 1][4] = 1
                error_list[i + 1][4] = ((test_min_torque - float(combine_torque.iloc[i, 2])) / float(
                    combine_torque.iloc[i, 2])) * 100

        return status_torque_list, error_list

    def status_torque_gain(self, combine_torque_gain):
        tolerance_torque = 0.1

        status_torque_list = [[3 for col in range(11)] for row in range(8)]
        status_gain_list = [[3 for col in range(11)] for row in range(8)]
        error_list = [[3 for col in range(11)] for row in range(8)]

        for i in range(1, 7):
            target_max_torque = float(combine_torque_gain.iloc[i, 1]) + float(
                combine_torque_gain.iloc[i, 1]) * tolerance_torque
            target_min_torque = float(combine_torque_gain.iloc[i, 2]) + float(
                combine_torque_gain.iloc[i, 2]) * tolerance_torque
            test_max_torque, test_min_torque = float(combine_torque_gain.iloc[i, 3]), float(
                combine_torque_gain.iloc[i, 4])
            target_kp, target_kv, target_kl2 = float(combine_torque_gain.iloc[i, 5]), float(
                combine_torque_gain.iloc[i, 6]), float(combine_torque_gain.iloc[i, 7])
            test_kp, test_kv, test_kl2 = float(combine_torque_gain.iloc[i, 8]), float(
                combine_torque_gain.iloc[i, 9]), float(combine_torque_gain.iloc[i, 10])

            if test_max_torque <= target_max_torque:
                status_torque_list[i + 1][3] = 0
            else:
                status_torque_list[i + 1][3] = 1
                error_list[i + 1][3] = ((test_max_torque - float(combine_torque_gain.iloc[i, 1])) / float(
                    combine_torque_gain.iloc[i, 1])) * 100
            if test_min_torque >= target_min_torque:
                status_torque_list[i + 1][4] = 0
            else:
                status_torque_list[i + 1][4] = 1
                error_list[i + 1][4] = ((test_min_torque - float(combine_torque_gain.iloc[i, 2])) / float(
                    combine_torque_gain.iloc[i, 2])) * 100
            if test_kp == target_kp:
                status_gain_list[i + 1][8] = 0
            else:
                status_gain_list[i + 1][8] = 1

            if test_kv == target_kv:
                status_gain_list[i + 1][9] = 0
            else:
                status_gain_list[i + 1][9] = 1

            if test_kl2 == target_kl2:
                status_gain_list[i + 1][10] = 0
            else:
                status_gain_list[i + 1][10] = 1

        return status_torque_list, status_gain_list, error_list

    def status_trans_error(self, combine_trans):
        tolerance_trans = 0.1
        status_list = [[3 for col in range(5)] for row in range(5)]
        error_list = [[3 for col in range(5)] for row in range(5)]

        for i in range(1, 4):
            target_rms_trans = float(combine_trans.iloc[i, 1]) + float(combine_trans.iloc[i, 1]) * tolerance_trans
            target_max_trans = float(combine_trans.iloc[i, 2]) + float(combine_trans.iloc[i, 2]) * tolerance_trans
            test_rms_trans, test_max_trans = float(combine_trans.iloc[i, 3]), float(combine_trans.iloc[i, 4])

            if test_rms_trans <= target_rms_trans:
                status_list[i + 1][3] = 0
            else:
                status_list[i + 1][3] = 1
                error_list[i + 1][3] = (((test_rms_trans - float(combine_trans.iloc[i, 1])) / float(
                    combine_trans.iloc[i, 1])) * 100)
            if test_max_trans <= target_max_trans:
                status_list[i + 1][4] = 0
            else:
                status_list[i + 1][4] = 1
                error_list[i + 1][4] = (((test_max_trans - float(combine_trans.iloc[i, 2])) / float(
                    combine_trans.iloc[i, 2])) * 100)
        return status_list, error_list

    def status_rot_error(self, combine_rot):
        tolerance_rot = 0.1
        status_list = [[3 for col in range(5)] for row in range(5)]
        error_list = [[3 for col in range(5)] for row in range(5)]
        for i in range(1, 4):
            target_rms_rot = float(combine_rot.iloc[i, 1]) + float(combine_rot.iloc[i, 1]) * tolerance_rot
            target_max_rot = float(combine_rot.iloc[i, 2]) + float(combine_rot.iloc[i, 2]) * tolerance_rot
            test_rms_rot, test_max_rot = float(combine_rot.iloc[i, 3]), float(combine_rot.iloc[i, 4])

            if test_rms_rot <= target_rms_rot:
                status_list[i + 1][3] = 0
            else:
                status_list[i + 1][3] = 1
                error_list[i + 1][3] = (
                        ((test_rms_rot - float(combine_rot.iloc[i, 1])) / float(combine_rot.iloc[i, 1])) * 100)
            if test_max_rot <= target_max_rot:
                status_list[i + 1][4] = 0
            else:
                status_list[i + 1][4] = 1
                error_list[i + 1][4] = (
                        ((test_max_rot - float(combine_rot.iloc[i, 2])) / float(combine_rot.iloc[i, 2])) * 100)
        return status_list, error_list

    def status_gain(self, combine_gain):
        status_list = [[3 for col in range(7)] for row in range(8)]

        for i in range(1, 7):
            target_kp, target_kv, target_kl2 = float(combine_gain.iloc[i, 1]), float(combine_gain.iloc[i, 2]), float(
                combine_gain.iloc[i, 3])
            test_kp, test_kv, test_kl2 = float(combine_gain.iloc[i, 4]), float(combine_gain.iloc[i, 5]), float(
                combine_gain.iloc[i, 6])

            if test_kp == target_kp:
                status_list[i + 1][4] = 0
            else:
                status_list[i + 1][4] = 1

            if test_kv == target_kv:
                status_list[i + 1][5] = 0
            else:
                status_list[i + 1][5] = 1

            if test_kl2 == target_kl2:
                status_list[i + 1][6] = 0
            else:
                status_list[i + 1][6] = 1

        return status_list

    # Create each result tables
    def create_joint_table(self, df, title_text, title_align):
        # Title for the table
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            name='CenteredTitle',
            parent=styles['Heading3'],
            alignment=title_align
        )
        centered_title = Paragraph(title_text, title_style)
        # Convert DataFrame to a list of lists for ReportLab Table
        data = [df.columns.to_list()] + df.values.tolist()
        table = Table(data)

        style_list = [
            ('SPAN', (1, 0), (2, 0)), ('SPAN', (3, 0), (4, 0)),
            ('SPAN', (5, 0), (6, 0)), ('SPAN', (7, 0), (8, 0)),
            ('BACKGROUND', (0, 0), (-1, 1), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 1), 'CENTRE'),
            ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
            # ('BOTTOMPADDING', (0, 0), (-1, 1), 6),
            ('BACKGROUND', (0, 2), (0, -1), colors.beige),
            ('BACKGROUND', (1, 2), (2, -1), colors.azure),
            ('BACKGROUND', (3, 2), (4, -1), colors.antiquewhite),
            ('BACKGROUND', (5, 2), (6, -1), colors.azure),
            ('BACKGROUND', (7, 2), (8, -1), colors.antiquewhite),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]
        # Add style to the table
        table.setStyle(TableStyle(style_list))

        status_list, error_list = self.status_joint_error(df)
        for i in range(len(status_list)):
            for j in range(len(status_list[i])):
                if status_list[i][j] == 1:
                    table.setStyle(TableStyle([('TEXTCOLOR', (j, i), (j, i), colors.red)]))

        return [centered_title, Spacer(1, 3), table]

    def create_torque_table(self, df, title_text, title_align):
        # Title for the table
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            name='CenteredTitle',
            parent=styles['Heading3'],
            alignment=title_align
        )
        centered_title = Paragraph(title_text, title_style)
        # Convert DataFrame to a list of lists for ReportLab Table
        data = [df.columns.to_list()] + df.values.tolist()
        table = Table(data)

        # Add style to the table
        style_list = [
            ('SPAN', (1, 0), (2, 0)), ('SPAN', (3, 0), (4, 0)),
            ('BACKGROUND', (0, 0), (-1, 1), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 1), colors.whitesmoke),
            ('TEXTCOLOR', (0, 2), (-1, 1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 1), 'CENTRE'),
            ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 2), (0, -1), colors.beige),
            ('BACKGROUND', (1, 2), (2, -1), colors.azure),
            ('BACKGROUND', (3, 2), (4, -1), colors.antiquewhite),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]
        table.setStyle(TableStyle(style_list))

        status_torque_list, error_list = self.status_torque(df)

        for i in range(len(status_torque_list)):
            for j in range(len(status_torque_list[i])):
                if status_torque_list[i][j] == 1:
                    table.setStyle(TableStyle([('TEXTCOLOR', (j, i), (j, i), colors.red)]))

        return [centered_title, Spacer(1, 3), table]

    def create_torque_gain_table(self, df, title_text, title_align):
        # Title for the table
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            name='CenteredTitle',
            parent=styles['Heading3'],
            alignment=title_align
        )
        centered_title = Paragraph(title_text, title_style)
        # Convert DataFrame to a list of lists for ReportLab Table
        data = [df.columns.to_list()] + df.values.tolist()
        table = Table(data)

        # Add style to the table
        style_list = [
            ('SPAN', (1, 0), (2, 0)), ('SPAN', (3, 0), (4, 0)),
            ('SPAN', (5, 0), (7, 0)), ('SPAN', (8, 0), (10, 0)),
            ('BACKGROUND', (0, 0), (-1, 1), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 1), colors.whitesmoke),
            ('TEXTCOLOR', (0, 2), (-1, 1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 1), 'CENTRE'),
            ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 2), (0, -1), colors.beige),
            ('BACKGROUND', (1, 2), (2, -1), colors.azure),
            ('BACKGROUND', (3, 2), (4, -1), colors.antiquewhite),
            ('BACKGROUND', (5, 2), (7, -1), colors.azure),
            ('BACKGROUND', (8, 2), (10, -1), colors.antiquewhite),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]
        table.setStyle(TableStyle(style_list))

        status_torque_list, status_gain_list, error_list = self.status_torque_gain(df)

        for i in range(len(status_torque_list)):
            for j in range(len(status_torque_list[i])):
                if status_torque_list[i][j] == 1:
                    table.setStyle(TableStyle([('TEXTCOLOR', (j, i), (j, i), colors.red)]))

        for i in range(len(status_gain_list)):
            for j in range(len(status_gain_list[i])):
                if status_gain_list[i][j] == 1:
                    table.setStyle(TableStyle([('TEXTCOLOR', (j, i), (j, i), colors.blue)]))

        return [centered_title, Spacer(1, 3), table]

    def create_trans_table(self, df, title_text, title_align):
        # Title for the table
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            name='CenteredTitle',
            parent=styles['Heading3'],
            alignment=title_align
        )
        centered_title = Paragraph(title_text, title_style)
        # Convert DataFrame to a list of lists for ReportLab Table
        data = [df.columns.to_list()] + df.values.tolist()
        table = Table(data)

        # Add style to the table
        style_list = [
            ('SPAN', (1, 0), (2, 0)), ('SPAN', (3, 0), (4, 0)),
            ('BACKGROUND', (0, 0), (-1, 1), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 1), colors.whitesmoke),
            ('TEXTCOLOR', (0, 2), (-1, 1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 1), 'CENTRE'),
            ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 2), (0, -1), colors.beige),
            ('BACKGROUND', (1, 2), (2, -1), colors.azure),
            ('BACKGROUND', (3, 2), (4, -1), colors.antiquewhite),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]
        table.setStyle(TableStyle(style_list))

        status_trans_list, error_list = self.status_trans_error(df)

        for i in range(len(status_trans_list)):
            for j in range(len(status_trans_list[i])):
                if status_trans_list[i][j] == 1:
                    table.setStyle(TableStyle([('TEXTCOLOR', (j, i), (j, i), colors.red)]))

        return [centered_title, Spacer(1, 12), table]

    def create_rot_table(self, df, title_text, title_align):
        # Title for the table
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            name='CenteredTitle',
            parent=styles['Heading3'],
            alignment=title_align
        )
        centered_title = Paragraph(title_text, title_style)
        # Convert DataFrame to a list of lists for ReportLab Table
        data = [df.columns.to_list()] + df.values.tolist()
        table = Table(data)

        # Add style to the table
        style_list = [
            ('SPAN', (1, 0), (2, 0)), ('SPAN', (3, 0), (4, 0)),
            ('BACKGROUND', (0, 0), (-1, 1), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 1), colors.whitesmoke),
            ('TEXTCOLOR', (0, 2), (-1, 1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 1), 'CENTRE'),
            ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 2), (0, -1), colors.beige),
            ('BACKGROUND', (1, 2), (2, -1), colors.azure),
            ('BACKGROUND', (3, 2), (4, -1), colors.antiquewhite),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]
        table.setStyle(TableStyle(style_list))

        status_rot_list, error_list = self.status_rot_error(df)

        for i in range(len(status_rot_list)):
            for j in range(len(status_rot_list[i])):
                if status_rot_list[i][j] == 1:
                    table.setStyle(TableStyle([('TEXTCOLOR', (j, i), (j, i), colors.red)]))
        return [centered_title, Spacer(1, 12), table]

    def create_gain_table(self, df, title_text, title_align):
        # Title for the table
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            name='CenteredTitle',
            parent=styles['Heading3'],
            alignment=title_align
        )
        centered_title = Paragraph(title_text, title_style)
        # Convert DataFrame to a list of lists for ReportLab Table
        data = [df.columns.to_list()] + df.values.tolist()
        table = Table(data)

        # Add style to the table
        style_list = [
            ('SPAN', (1, 0), (3, 0)), ('SPAN', (4, 0), (6, 0)),
            ('BACKGROUND', (0, 0), (-1, 1), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 1), colors.whitesmoke),
            ('TEXTCOLOR', (0, 2), (-1, 1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 1), 'CENTRE'),
            ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 2), (0, -1), colors.beige),
            ('BACKGROUND', (1, 2), (3, -1), colors.azure),
            ('BACKGROUND', (4, 2), (6, -1), colors.antiquewhite),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]
        table.setStyle(TableStyle(style_list))

        status_gain_list = self.status_gain(df)

        for i in range(len(status_gain_list)):
            for j in range(len(status_gain_list[i])):
                if status_gain_list[i][j] == 1:
                    table.setStyle(TableStyle([('TEXTCOLOR', (j, i), (j, i), colors.blue)]))

        return [centered_title, Spacer(1, 12), table]

    # Generate result Plot & PDF on STEP
    def gen_report_step(self):
        self.load_data_6dof_step()

        if self.category == 'joint_motion':
            position_errors = self.extract_errors_for_all_joints()  # Position errors
            velocity_errors = self.extract_vel_errors_for_all_joints()  # Velocity errors
            torques = self.extract_torque_all_joints()

            image_paths = []
            pos_image_list = []
            for joint_number in range(1, 7):  # Assuming joint numbers are 1 through 6
                pos_file_name = f'Joint_{joint_number}_Pose_Tracking_Error.png'
                image_path = os.path.join(self.result_path, pos_file_name)
                # Append the path to the list
                pos_image = Img.open(image_path)
                pos_image_list.append(pos_image)
                if len(pos_image_list) == 2:
                    new_pos_image = Img.new('RGB', (2 * 640, 480))
                    new_pos_image.paste(pos_image_list[0], (0, 0))
                    new_pos_image.paste(pos_image_list[1], (640, 0))
                    pos_combine_name = f'Joint_combine{joint_number}_Pose_Tracking_Error.png'
                    pos_image_path = os.path.join(self.result_path, pos_combine_name)
                    new_pos_image.save(pos_image_path, "png")
                    pos_image_list = []
                    image_paths.append(pos_image_path)

            vel_image_list = []
            for joint_number in range(1, 7):  # Assuming joint numbers are 1 through 6
                vel_file_name = f'Joint_{joint_number}_Vel_Tracking_Error.png'
                image_path = os.path.join(self.result_path, vel_file_name)
                # Append the path to the list
                vel_image = Img.open(image_path)
                vel_image_list.append(vel_image)
                if len(vel_image_list) == 2:
                    new_vel_image = Img.new('RGB', (2 * 640, 480))
                    new_vel_image.paste(vel_image_list[0], (0, 0))
                    new_vel_image.paste(vel_image_list[1], (640, 0))
                    vel_combine_name = f'Joint_combine{joint_number}_Vel_Tracking_Error.png'
                    vel_image_path = os.path.join(self.result_path, vel_combine_name)
                    new_vel_image.save(vel_image_path, "png")
                    vel_image_list = []
                    image_paths.append(vel_image_path)

            tor_image_list = []
            for joint_number in range(1, 7):  # Assuming joint numbers are 1 through 6
                file_name = f'Joint_{joint_number}_Torque.png'
                image_path = os.path.join(self.result_path, file_name)
                # Append the path to the list
                tor_image = Img.open(image_path)
                tor_image_list.append(tor_image)
                if len(tor_image_list) == 2:
                    new_tor_image = Img.new('RGB', (2 * 640, 480))
                    new_tor_image.paste(tor_image_list[0], (0, 0))
                    new_tor_image.paste(tor_image_list[1], (640, 0))
                    tor_combine_name = f'Joint_combine{joint_number}_Torque.png'
                    tor_image_path = os.path.join(self.result_path, tor_combine_name)
                    new_tor_image.save(tor_image_path, "png")
                    tor_image_list = []
                    image_paths.append(tor_image_path)

            pos_list = []
            for joint_number in range(1, 7):  # Assuming joint numbers are 1 through 6
                self.plot_position_plt(joint_number)
                file_name = f'Joint_{joint_number}_Position.png'
                image_path = os.path.join(self.result_path, file_name)
                # Append the path to the list
                pos_image = Img.open(image_path)
                pos_list.append(pos_image)
                if len(pos_list) == 2:
                    new_pos_image = Img.new('RGB', (2 * 640, 480))
                    new_pos_image.paste(pos_list[0], (0, 0))
                    new_pos_image.paste(pos_list[1], (640, 0))
                    pos_combine_name = f'Joint_combine{joint_number}_Position.png'
                    pos_image_path = os.path.join(self.result_path, pos_combine_name)
                    new_pos_image.save(pos_image_path, "png")
                    pos_list = []
                    image_paths.append(pos_image_path)

            vel_list = []
            for joint_number in range(1, 7):  # Assuming joint numbers are 1 through 6
                self.plot_velocity_plt(joint_number)
                file_name = f'Joint_{joint_number}_Velocity.png'
                image_path = os.path.join(self.result_path, file_name)
                # Append the path to the list
                vel_image = Img.open(image_path)
                vel_list.append(vel_image)
                if len(vel_list) == 2:
                    new_vel_image = Img.new('RGB', (2 * 640, 480))
                    new_vel_image.paste(vel_list[0], (0, 0))
                    new_vel_image.paste(vel_list[1], (640, 0))
                    vel_combine_name = f'Joint_combine{joint_number}_Velocity.png'
                    vel_image_path = os.path.join(self.result_path, vel_combine_name)
                    new_vel_image.save(vel_image_path, "png")
                    vel_list = []
                    image_paths.append(vel_image_path)

            fric_list = []
            for joint_number in range(1, 7):  # Assuming joint numbers are 1 through 6
                self.plot_friction_plt(joint_number)
                file_name = f'Joint_{joint_number}_Friction.png'
                image_path = os.path.join(self.result_path, file_name)
                # Append the path to the list
                fric_image = Img.open(image_path)
                fric_list.append(fric_image)
                if len(fric_list) == 2:
                    new_fric_image = Img.new('RGB', (2 * 640, 480))
                    new_fric_image.paste(fric_list[0], (0, 0))
                    new_fric_image.paste(fric_list[1], (640, 0))
                    fric_combine_name = f'Joint_combine{joint_number}_Friction.png'
                    fric_image_path = os.path.join(self.result_path, fric_combine_name)
                    new_fric_image.save(fric_image_path, "png")
                    fric_list = []
                    image_paths.append(fric_image_path)

            force_list = []
            for joint_number in range(1, 7):  # Assuming joint numbers are 1 through 6
                self.plot_force_plt(joint_number)
                file_name = f'Joint_{joint_number}_Force.png'
                image_path = os.path.join(self.result_path, file_name)
                # Append the path to the list
                force_image = Img.open(image_path)
                force_list.append(force_image)
                if len(force_list) == 2:
                    new_force_image = Img.new('RGB', (2 * 640, 480))
                    new_force_image.paste(force_list[0], (0, 0))
                    new_force_image.paste(force_list[1], (640, 0))
                    force_combine_name = f'Joint_combine{joint_number}_Force.png'
                    force_image_path = os.path.join(self.result_path, force_combine_name)
                    new_force_image.save(force_image_path, "png")
                    force_list = []
                    image_paths.append(force_image_path)

            test_info = {
                "motion_type": self.category,
                "robot_name": self.robot_name
            }

            pdf_name = f"{self.robot_name}_joint_motion_report.pdf"
            pdf_path = os.path.join(self.result_path, pdf_name)
            critia = self.benchmark_critia

            self.gen_joint_pdf_report_step(critia, position_errors, velocity_errors, torques, test_info, pdf_path,
                                           image_paths)

        if self.category == 'task_motion':
            translation_errors, rotation_errors = self.extract_errors_translation_rotation()
            torques = self.extract_torque_all_joints()

            image_paths = []
            task_image_list = []
            file_name = f'X_Translation_Error.png'
            image_path = os.path.join(self.result_path, file_name)
            task_image = Img.open(image_path)
            task_image_list.append(task_image)

            file_name = f'U_Rotation_Error.png'
            image_path = os.path.join(self.result_path, file_name)
            task_image = Img.open(image_path)
            task_image_list.append(task_image)

            new_task_image = Img.new('RGB', (2 * 640, 480))
            new_task_image.paste(task_image_list[0], (0, 0))
            new_task_image.paste(task_image_list[1], (640, 0))
            new_image_name = 'XU_Error.png'
            new_image_path = os.path.join(self.result_path, new_image_name)
            new_task_image.save(new_image_path, "png")
            task_image_list = []
            image_paths.append(new_image_path)

            file_name = f'Y_Translation_Error.png'
            image_path = os.path.join(self.result_path, file_name)
            task_image = Img.open(image_path)
            task_image_list.append(task_image)

            file_name = f'V_Rotation_Error.png'
            image_path = os.path.join(self.result_path, file_name)
            task_image = Img.open(image_path)
            task_image_list.append(task_image)

            new_task_image = Img.new('RGB', (2 * 640, 480))
            new_task_image.paste(task_image_list[0], (0, 0))
            new_task_image.paste(task_image_list[1], (640, 0))
            new_image_name = 'YV_Error.png'
            new_image_path = os.path.join(self.result_path, new_image_name)
            new_task_image.save(new_image_path, "png")
            task_image_list = []
            image_paths.append(new_image_path)

            file_name = f'Z_Translation_Error.png'
            image_path = os.path.join(self.result_path, file_name)
            # Append the path to the list
            task_image = Img.open(image_path)
            task_image_list.append(task_image)

            file_name = f'W_Rotation_Error.png'
            image_path = os.path.join(self.result_path, file_name)
            # Append the path to the list
            task_image = Img.open(image_path)
            task_image_list.append(task_image)

            new_task_image = Img.new('RGB', (2 * 640, 480))
            new_task_image.paste(task_image_list[0], (0, 0))
            new_task_image.paste(task_image_list[1], (640, 0))
            new_image_name = 'ZW_Error.png'
            new_image_path = os.path.join(self.result_path, new_image_name)
            new_task_image.save(new_image_path, "png")
            task_image_list = []
            image_paths.append(new_image_path)

            tor_image_list = []
            for joint_number in range(1, 7):  # Assuming joint numbers are 1 through 6
                file_name = f'Joint_{joint_number}_Torque.png'
                image_path = os.path.join(self.result_path, file_name)
                # Append the path to the list
                tor_image = Img.open(image_path)
                tor_image_list.append(tor_image)
                if len(tor_image_list) == 2:
                    new_tor_image = Img.new('RGB', (2 * 640, 480))
                    new_tor_image.paste(tor_image_list[0], (0, 0))
                    new_tor_image.paste(tor_image_list[1], (640, 0))
                    tor_combine_name = f'Joint_combine{joint_number}_Torque.png'
                    tor_image_path = os.path.join(self.result_path, tor_combine_name)
                    new_tor_image.save(tor_image_path, "png")
                    tor_image_list = []
                    image_paths.append(tor_image_path)

            pos_list = []
            for joint_number in range(1, 7):  # Assuming joint numbers are 1 through 6
                self.plot_position_plt(joint_number)
                file_name = f'Joint_{joint_number}_Position.png'
                image_path = os.path.join(self.result_path, file_name)
                # Append the path to the list
                pos_image = Img.open(image_path)
                pos_list.append(pos_image)
                if len(pos_list) == 2:
                    new_pos_image = Img.new('RGB', (2 * 640, 480))
                    new_pos_image.paste(pos_list[0], (0, 0))
                    new_pos_image.paste(pos_list[1], (640, 0))
                    pos_combine_name = f'Joint_combine{joint_number}_Position.png'
                    pos_image_path = os.path.join(self.result_path, pos_combine_name)
                    new_pos_image.save(pos_image_path, "png")
                    pos_list = []
                    image_paths.append(pos_image_path)

            vel_list = []
            for joint_number in range(1, 7):  # Assuming joint numbers are 1 through 6
                self.plot_velocity_plt(joint_number)
                file_name = f'Joint_{joint_number}_Velocity.png'
                image_path = os.path.join(self.result_path, file_name)
                # Append the path to the list
                vel_image = Img.open(image_path)
                vel_list.append(vel_image)
                if len(vel_list) == 2:
                    new_vel_image = Img.new('RGB', (2 * 640, 480))
                    new_vel_image.paste(vel_list[0], (0, 0))
                    new_vel_image.paste(vel_list[1], (640, 0))
                    vel_combine_name = f'Joint_combine{joint_number}_Velocity.png'
                    vel_image_path = os.path.join(self.result_path, vel_combine_name)
                    new_vel_image.save(vel_image_path, "png")
                    vel_list = []
                    image_paths.append(vel_image_path)

            fric_list = []
            for joint_number in range(1, 7):  # Assuming joint numbers are 1 through 6
                self.plot_friction_plt(joint_number)
                file_name = f'Joint_{joint_number}_Friction.png'
                image_path = os.path.join(self.result_path, file_name)
                # Append the path to the list
                fric_image = Img.open(image_path)
                fric_list.append(fric_image)
                if len(fric_list) == 2:
                    new_fric_image = Img.new('RGB', (2 * 640, 480))
                    new_fric_image.paste(fric_list[0], (0, 0))
                    new_fric_image.paste(fric_list[1], (640, 0))
                    fric_combine_name = f'Joint_combine{joint_number}_Friction.png'
                    fric_image_path = os.path.join(self.result_path, fric_combine_name)
                    new_fric_image.save(fric_image_path, "png")
                    fric_list = []
                    image_paths.append(fric_image_path)

            force_list = []
            for joint_number in range(1, 7):  # Assuming joint numbers are 1 through 6
                self.plot_force_plt(joint_number)
                file_name = f'Joint_{joint_number}_Force.png'
                image_path = os.path.join(self.result_path, file_name)
                # Append the path to the list
                force_image = Img.open(image_path)
                force_list.append(force_image)
                if len(force_list) == 2:
                    new_force_image = Img.new('RGB', (2 * 640, 480))
                    new_force_image.paste(force_list[0], (0, 0))
                    new_force_image.paste(force_list[1], (640, 0))
                    force_combine_name = f'Joint_combine{joint_number}_Force.png'
                    force_image_path = os.path.join(self.result_path, force_combine_name)
                    new_force_image.save(force_image_path, "png")
                    force_list = []
                    image_paths.append(force_image_path)

            self.plot_task_motion_2D_plt("XY")
            self.plot_task_motion_2D_plt("YZ")
            self.plot_task_motion_2D_plt("XZ")
            self.plot_task_motion_3D_plt()

            file_name = f'Task Space Tracking XY.png'
            image_path = os.path.join(self.result_path, file_name)
            # Append the path to the list
            task_image = Img.open(image_path)
            task_image_list.append(task_image)

            file_name = f'Task Space Tracking YZ.png'
            image_path = os.path.join(self.result_path, file_name)
            # Append the path to the list
            task_image = Img.open(image_path)
            task_image_list.append(task_image)

            new_task_image = Img.new('RGB', (2 * 640, 480))
            new_task_image.paste(task_image_list[0], (0, 0))
            new_task_image.paste(task_image_list[1], (640, 0))
            new_image_name = 'XY_Error.png'
            new_image_path = os.path.join(self.result_path, new_image_name)
            new_task_image.save(new_image_path, "png")
            task_image_list = []
            image_paths.append(new_image_path)

            file_name = f'Task Space Tracking XZ.png'
            image_path = os.path.join(self.result_path, file_name)
            # Append the path to the list
            task_image = Img.open(image_path)
            task_image_list.append(task_image)

            file_name = 'Task Space Tracking 3D.png'
            image_path = os.path.join(self.result_path, file_name)
            # Append the path to the list
            task_image = Img.open(image_path)
            task_image_list.append(task_image)

            new_task_image = Img.new('RGB', (2 * 640, 480))
            new_task_image.paste(task_image_list[0], (0, 0))
            new_task_image.paste(task_image_list[1], (640, 0))
            new_image_name = '3D_Error.png'
            new_image_path = os.path.join(self.result_path, new_image_name)
            new_task_image.save(new_image_path, "png")
            task_image_list = []
            image_paths.append(new_image_path)

            test_info = {
                "motion_type": self.category,
                "robot_name": self.robot_name,
            }

            pdf_name = f"{self.robot_name}_task_motion_report.pdf"
            pdf_path = os.path.join(self.result_path, pdf_name)
            critia = self.benchmark_critia

            self.gen_task_pdf_report_step(critia, translation_errors, rotation_errors, test_info, pdf_path, image_paths)

    def gen_joint_pdf_report_step(self, critia, position_errors, velocity_errors, torques, test_info, pdf_path,
                                  image_path):
        # Create DataFrames
        df_pos = pd.DataFrame(position_errors).T
        df_vel = pd.DataFrame(velocity_errors).T
        df_torque = pd.DataFrame(torques).T

        critia_df_pos = pd.DataFrame(critia['benchmark_pos']).T
        critia_df_vel = pd.DataFrame(critia['benchmark_vel']).T
        critia_df_torque = pd.DataFrame(critia['benchmark_torque']).T

        df_pos['RMS Error (deg)'] = df_pos['RMS Error']
        df_pos['Max Error (deg)'] = df_pos['Max Error']
        df_vel['RMS Error (deg/s)'] = df_vel['RMS Error']
        df_vel['Max Error (deg/s)'] = df_vel['Max Error']

        df_pos['RMS Error'] = df_pos['RMS Error'].apply(lambda x: f'{x:.3e}')
        df_pos['Max Error'] = df_pos['Max Error'].apply(lambda x: f'{x:.3e}')
        df_pos['RMS Error (deg)'] = df_pos['RMS Error (deg)'].apply(lambda x: f'{x:.3e}')
        df_pos['Max Error (deg)'] = df_pos['Max Error (deg)'].apply(lambda x: f'{x:.3e}')

        df_vel['RMS Error'] = df_vel['RMS Error'].apply(lambda x: f'{x:.3e}')
        df_vel['Max Error'] = df_vel['Max Error'].apply(lambda x: f'{x:.3e}')
        df_vel['RMS Error (deg/s)'] = df_vel['RMS Error (deg/s)'].apply(lambda x: f'{x:.3e}')
        df_vel['Max Error (deg/s)'] = df_vel['Max Error (deg/s)'].apply(lambda x: f'{x:.3e}')

        critia_df_pos['RMS Error (deg)'] = critia_df_pos['RMS Error']
        critia_df_pos['Max Error (deg)'] = critia_df_pos['Max Error']
        critia_df_vel['RMS Error (deg/s)'] = critia_df_vel['RMS Error']
        critia_df_vel['Max Error (deg/s)'] = critia_df_vel['Max Error']

        critia_df_pos['RMS Error'] = critia_df_pos['RMS Error'].apply(lambda x: f'{x:.3e}')
        critia_df_pos['Max Error'] = critia_df_pos['Max Error'].apply(lambda x: f'{x:.3e}')
        critia_df_pos['RMS Error (deg)'] = critia_df_pos['RMS Error (deg)'].apply(lambda x: f'{x:.3e}')
        critia_df_pos['Max Error (deg)'] = critia_df_pos['Max Error (deg)'].apply(lambda x: f'{x:.3e}')

        critia_df_vel['RMS Error'] = critia_df_vel['RMS Error'].apply(lambda x: f'{x:.3e}')
        critia_df_vel['Max Error'] = critia_df_vel['Max Error'].apply(lambda x: f'{x:.3e}')
        critia_df_vel['RMS Error (deg/s)'] = critia_df_vel['RMS Error (deg/s)'].apply(lambda x: f'{x:.3e}')
        critia_df_vel['Max Error (deg/s)'] = critia_df_vel['Max Error (deg/s)'].apply(lambda x: f'{x:.3e}')

        del df_pos['RMS Error'], df_pos['Max Error'], df_vel['RMS Error'], df_vel['Max Error']
        del critia_df_pos['RMS Error'], critia_df_pos['Max Error'], critia_df_vel['RMS Error'], critia_df_vel[
            'Max Error']

        df_torque['Max torque'] = df_torque['Max torque'].apply(lambda x: f'{x:.7}')
        df_torque['Min torque'] = df_torque['Min torque'].apply(lambda x: f'{x:.7}')
        critia_df_torque['Max torque'] = critia_df_torque['Max torque'].apply(lambda x: f'{x:.7}')
        critia_df_torque['Min torque'] = critia_df_torque['Min torque'].apply(lambda x: f'{x:.7}')

        combine_pos = pd.concat([critia_df_pos, df_pos], axis=1)
        combine_vel = pd.concat([critia_df_vel, df_vel], axis=1)
        combine_torque = pd.concat([critia_df_torque, df_torque], axis=1)

        combine_pos.index.name = 'Joint'
        combine_pos.reset_index(inplace=True)
        combine_pos = combine_pos.T
        combine_pos.reset_index(inplace=True)
        combine_pos = combine_pos.T
        combine_pos.loc['index'] = ['Joint', 'RMS Error', 'Max Error', 'RMS Error', 'Max Error']
        combine_pos = combine_pos.T
        combine_pos.columns = ['', '', '', '', '', '', '']
        combine_pos = combine_pos.T
        combine_pos.columns = ['', 'Target', 'Target', 'Test', 'Test']

        combine_vel = combine_vel.T
        combine_vel.reset_index(inplace=True)
        combine_vel = combine_vel.T
        combine_vel.loc['index'] = ['RMS Error', 'Max Error', 'RMS Error', 'Max Error']
        combine_vel = combine_vel.T
        combine_vel.columns = ['', '', '', '', '', '', '']
        combine_vel = combine_vel.T
        combine_vel.columns = ['Target', 'Target', 'Test', 'Test']

        combine_torque.index.name = 'Joint'
        combine_torque.reset_index(inplace=True)
        combine_torque = combine_torque.T
        combine_torque.reset_index(inplace=True)
        combine_torque = combine_torque.T
        combine_torque.loc['index'] = ['Joint', 'Max torque', 'Min torque', 'Max torque', 'Min torque']
        combine_torque = combine_torque.T
        combine_torque.columns = ['', '', '', '', '', '', '']
        combine_torque = combine_torque.T
        combine_torque.columns = ['', 'Target', 'Target', 'Test', 'Test']

        combine_error = pd.concat([combine_pos, combine_vel], axis=1)

        joint_status, error_joint = self.status_joint_error(combine_error)
        torque_status, error_torque = self.status_torque(combine_torque)

        # Extracting information from the test_info dictionary
        motion_type = test_info.get("motion_type", "Unknown motion")
        robot_name = test_info.get("robot_name", "Unknown Robot")

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            name='CenteredTitle',
            parent=styles['Heading2'],
            alignment=TA_LEFT
        )

        # Introductory information
        title = Paragraph("Robot Control Performance Report", styles['Title'])
        info_title = Paragraph("<b>1. Benchmark Information</b>", title_style)
        result_title = Paragraph("<b>2. Result Overview</b>", title_style)
        sub_title = Paragraph("<b>3. Result Tables</b>", title_style)
        pos_plot_title = Paragraph("<b>4. Joint Position Tracking Error Plot</b>", title_style)
        vel_plot_title = Paragraph("<b>5. Joint Velocity Tracking Error Plot</b>", title_style)
        torque_plot_title = Paragraph("<b>6. Joint Torque Plot</b>", title_style)
        pos_title = Paragraph("<b>7. Joint Position Plot</b>", title_style)
        vel_title = Paragraph("<b>8. Joint Velocity Plot</b>", title_style)
        fric_title = Paragraph("<b>9. Joint Friction Plot</b>", title_style)
        force_title = Paragraph("<b>10. Joint Force Plot</b>", title_style)

        first_info = Paragraph(f"<b>- Motion:</b> {motion_type}\
                            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                            &nbsp; <b>- Robot:</b> {robot_name}", styles['BodyText'])

        status_info = Paragraph(
            u"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>a. Overall Status: <font color='blue'>PASS</font></b> ",
            styles['BodyText'])

        tracking_table = self.create_joint_table(combine_error, "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                            &nbsp;&nbsp; Position Tracking Error (deg) &nbsp;&nbsp;&nbsp;\
                            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                            &nbsp;&nbsp;&nbsp; Velocity Tracking Error (deg/s)", TA_LEFT)
        torque_table = self.create_torque_table(combine_torque, "Joint Torque (Nm)", TA_CENTER)

        status_sign = False
        pos_rms_error_sign, pos_max_error_sign = False, False
        vel_rms_error_sign, vel_max_error_sign = False, False
        torque_max_sign, torque_min_sign = False, False
        pos_rms_error, pos_max_error = "", ""
        vel_rms_error, vel_max_error = "", ""
        torque_max_error, torque_min_error = "", ""

        for i in range(2, len(joint_status)):
            if joint_status[i][3] == 1:
                pos_rms_error += f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                                    - Joint_{i - 1}({error_joint[i][3]:.1f}%) <br/>"
                pos_rms_error_sign = True
                status_sign = True
            if joint_status[i][4] == 1:
                pos_max_error += f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                                    - Joint_{i - 1}({error_joint[i][4]:.1f}%) <br/>"
                pos_max_error_sign = True
                status_sign = True

            if joint_status[i][7] == 1:
                vel_rms_error += f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                                    - Joint_{i - 1}({error_joint[i][7]:.1f}%) <br/>"
                vel_rms_error_sign = True
                status_sign = True
            if joint_status[i][8] == 1:
                vel_max_error += f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                                    - Joint_{i - 1}({error_joint[i][8]:.1f}%) <br/>"
                vel_max_error_sign = True
                status_sign = True

        for i in range(2, len(torque_status)):
            if torque_status[i][3] == 1:
                torque_max_error += f"Joint_{i - 1}({error_torque[i][3]:.1f}%) "
                torque_max_sign = True
            if torque_status[i][4] == 1:
                torque_min_error += f"Joint_{i - 1}({error_torque[i][4]:.1f}%) "
                torque_min_sign = True

        if status_sign:
            status_info = Paragraph(u"&nbsp;&nbsp;&nbsp;&nbsp;<b>a. Overall Status: \
                                    <font color='red'>FAILED</font></b> ", styles['BodyText'])
        else:
            status_info = Paragraph(u"&nbsp;&nbsp;&nbsp;&nbsp;<b>a. Overall Status: \
                                    <font color='blue'>PASS</font></b> ", styles['BodyText'])

        # Build the PDF with the intro and tables
        elements = [title, Spacer(1, 20), info_title, Spacer(1, 5), first_info, Spacer(1, 20), result_title]

        # If status is FAIL, add error's detail
        pos_error_info = Paragraph("&nbsp;&nbsp;&nbsp;&nbsp<b>b. Position Tracking Error</b>",
                                   styles['BodyText'])
        elements += [Spacer(1, 5), status_info, Spacer(1, 10), pos_error_info]

        if pos_rms_error_sign:
            pos_rms_error_info = Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                                <b>i. RMS error exceeded the benchmark </b>", styles['BodyText'])
            pos_rms_error = Paragraph(pos_rms_error, styles['BodyText'])
            elements += [Spacer(1, 5), pos_rms_error_info, Spacer(1, 1), pos_rms_error]

        if pos_max_error_sign:
            pos_max_error_info = Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                                <b>ii. Max error exceeded the benchmark </b>", styles['BodyText'])
            pos_max_error = Paragraph(pos_max_error, styles['BodyText'])
            elements += [Spacer(1, 5), pos_max_error_info, Spacer(1, 1), pos_max_error]

        vel_error_info = Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;<b>c. Velocity Tracking Error</b>",
                                   styles['BodyText'])
        elements += [Spacer(1, 5), vel_error_info]

        if vel_rms_error_sign:
            vel_rms_error_info = Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                                <b>i. RMS error exceeded the benchmark </b>", styles['BodyText'])
            vel_rms_error = Paragraph(vel_rms_error, styles['BodyText'])
            elements += [Spacer(1, 5), vel_rms_error_info, Spacer(1, 1), vel_rms_error]
        if vel_max_error_sign:
            vel_max_error_info = Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                                <b>ii. Max error exceeded the benchmark </b>", styles['BodyText'])
            vel_max_error = Paragraph(vel_max_error, styles['BodyText'])
            elements += [Spacer(1, 5), vel_max_error_info, Spacer(1, 1), vel_max_error]

        recommand_info = Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;<b>d. Recommandations: </b> ",
                                   styles['BodyText'])
        torque_info = Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \
                                <b>i. Additional aging is recommended due to large joint torque</b>",
                                styles['BodyText'])
        elements += [Spacer(1, 5), recommand_info, Spacer(1, 5), torque_info]

        if torque_max_sign:
            torque_max = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>- Max torque: </b>" + torque_max_error
            torque_max_info = Paragraph(torque_max, styles['BodyText'])
            elements += [Spacer(1, 5), torque_max_info]
        if torque_min_sign:
            torque_min = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>- Min torque: </b>" + torque_min_error
            torque_min_info = Paragraph(torque_min, styles['BodyText'])
            elements += [Spacer(1, 5), torque_min_info]

        elements.append(PageBreak())

        # Add torque and gain table
        elements += [sub_title, Spacer(1, 5)] + tracking_table + [Spacer(1, 10)] + torque_table + [Spacer(1, 10)]

        elements.append(PageBreak())

        ############################### Position Error Plot ##################################
        elements += [pos_plot_title]
        elements.append(Image(image_path[0], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[1], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[2], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))

        elements.append(PageBreak())

        ############################### Velocity Error Plot ##################################
        elements += [vel_plot_title]
        elements.append(Image(image_path[3], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[4], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[5], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))

        elements.append(PageBreak())

        ################################### Torque Plot #######################################
        elements += [torque_plot_title]
        elements.append(Image(image_path[6], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[7], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[8], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))

        elements.append(PageBreak())

        ################################### Position Plot #####################################
        elements += [pos_title]
        elements.append(Image(image_path[9], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[10], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[11], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))

        elements.append(PageBreak())

        ################################### Velocity Plot #####################################
        elements += [vel_title]
        elements.append(Image(image_path[12], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[13], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[14], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))

        elements.append(PageBreak())

        ################################### Friction Plot #####################################
        elements += [fric_title]

        elements.append(Image(image_path[15], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[16], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[17], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))

        # Create a PDF document
        pdf = SimpleDocTemplate(pdf_path, pagesize=letter)

        # Make PDF
        pdf.build(elements, onFirstPage=self.addPageNumber, onLaterPages=self.addPageNumber)

    def gen_task_pdf_report_step(self, critia, translation_errors, rotation_errors, test_info, pdf_path, image_path):

        # Convert translation errors from meters to millimeters
        formatted_translation_errors = [[axis, rms * 1000, max_err * 1000] for axis, rms, max_err in translation_errors]
        formatted_translation_errors = [[axis, f'{rms:.3e}', f'{max_err:.3e}'] for axis, rms, max_err in
                                        formatted_translation_errors]
        formatted_rotation_errors = [[axis, f'{rms:.3e}', f'{max_err:.3e}'] for axis, rms, max_err in rotation_errors]

        critia_trans_errors = [[axis, rms * 1000, max_err * 1000] for axis, rms, max_err in critia['benchmark_trans']]
        critia_trans_errors = [[axis, f'{rms:.3e}', f'{max_err:.3e}'] for axis, rms, max_err in critia_trans_errors]
        critia_rot_errors = [[axis, f'{rms:.3e}', f'{max_err:.3e}'] for axis, rms, max_err in critia['benchmark_rot']]

        # Create DataFrames
        df_translation = pd.DataFrame(formatted_translation_errors, columns=['Axis', 'RMS Error', 'Max Error'])
        df_rotation = pd.DataFrame(formatted_rotation_errors, columns=['Axis', 'RMS Error', 'Max Error'])

        critia_trans = pd.DataFrame(critia_trans_errors, columns=['Axis', 'RMS Error', 'Max Error'])
        critia_rot = pd.DataFrame(critia_rot_errors, columns=['Axis', 'RMS Error', 'Max Error'])

        del df_translation['Axis'], df_rotation['Axis']

        combine_trans = pd.concat([critia_trans, df_translation], axis=1)
        combine_rot = pd.concat([critia_rot, df_rotation], axis=1)

        combine_trans = combine_trans.T
        combine_trans.reset_index(inplace=True)
        combine_trans.columns = ['', '', '', '']
        combine_trans = combine_trans.T
        combine_trans.columns = ['', 'Target', 'Target', 'Test', 'Test']

        combine_rot = combine_rot.T
        combine_rot.reset_index(inplace=True)
        combine_rot.columns = ['', '', '', '']
        combine_rot = combine_rot.T
        combine_rot.columns = ['', 'Target', 'Target', 'Test', 'Test']

        trans_status, error_trans = self.status_trans_error(combine_trans)
        rot_status, error_rot = self.status_rot_error(combine_rot)

        # Extracting information from the test_info dictionary
        motion_type = test_info.get("motion_type", "Unknown motion")
        robot_name = test_info.get("robot_name", "Unknown Robot")

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            name='CenteredTitle',
            parent=styles['Heading2'],
            alignment=TA_LEFT
        )

        # Introductory information
        title = Paragraph("Robot Control Performance Report", styles['Title'])
        info_title = Paragraph("<b>1. Benchmark Information</b>", title_style)
        result_title = Paragraph("<b>2. Result Overview</b>", title_style)
        sub_title = Paragraph("<b>3. Result Tables</b>", title_style)
        plot_title = Paragraph("<b>4. Error Plot</b>", title_style)
        task_title = Paragraph("<b>5. Task Space Tracking Plot</b>", title_style)
        torque_plot_title = Paragraph("<b>7. Joint Torque Plot</b>", title_style)
        pos_title = Paragraph("<b>8. Joint Position Plot</b>", title_style)
        vel_title = Paragraph("<b>9. Joint Velocity Plot</b>", title_style)
        fric_title = Paragraph("<b>10. Joint Friction Plot</b>", title_style)
        force_title = Paragraph("<b>11. Joint Force Plot</b>", title_style)

        first_info = Paragraph(f"<b>- Motion:</b> {motion_type}\
                            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                            &nbsp; <b>- Robot:</b> {robot_name}", styles['BodyText'])

        status_info = Paragraph(
            u"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>a. Overall Status: <font color='blue'>PASS</font></b> ",
            styles['BodyText'])

        trans_table = self.create_trans_table(combine_trans, "Translation Error (mm)", TA_CENTER)
        rot_table = self.create_rot_table(combine_rot, "Rotation Error (°)", TA_CENTER)

        status_sign = False
        trans_rms_error_sign, trans_max_error_sign = False, False
        rot_rms_error_sign, rot_max_error_sign = False, False
        trans_rms_error, trans_max_error = "", ""
        rot_rms_error, rot_max_error = "", ""

        if trans_status[2][3] == 1:
            trans_rms_error += f"X({error_trans[2][3]:.1f}%) "
            trans_rms_error_sign = True
            status_sign = True
        if trans_status[3][3] == 1:
            trans_rms_error += f"Y({error_trans[3][3]:.1f}%) "
            trans_rms_error_sign = True
            status_sign = True
        if trans_status[4][3] == 1:
            trans_rms_error += f"Z({error_trans[4][3]:.1f}%) "
            trans_rms_error_sign = True
            status_sign = True

        if trans_status[2][4] == 1:
            trans_max_error += f"X({error_trans[2][4]:.1f}%) "
            trans_max_error_sign = True
            status_sign = True
        if trans_status[3][4] == 1:
            trans_max_error += f"Y({error_trans[3][4]:.1f}%) "
            trans_max_error_sign = True
            status_sign = True
        if trans_status[4][4] == 1:
            trans_max_error += f"Z({error_trans[4][4]:.1f}%) "
            trans_max_error_sign = True
            status_sign = True

        if rot_status[2][3] == 1:
            rot_rms_error += f"U({error_rot[2][3]:.1f}%) "
            rot_rms_error_sign = True
            status_sign = True
        if rot_status[3][3] == 1:
            rot_rms_error += f"V({error_rot[3][3]:.1f}%) "
            rot_rms_error_sign = True
            status_sign = True
        if rot_status[4][3] == 1:
            rot_rms_error += f"W({error_rot[4][3]:.1f}%) "
            rot_rms_error_sign = True
            status_sign = True

        if rot_status[2][4] == 1:
            rot_max_error += f"U({error_rot[2][4]:.1f}%) "
            rot_max_error_sign = True
            status_sign = True
        if rot_status[3][4] == 1:
            rot_max_error += f"V({error_rot[3][4]:.1f}%) "
            rot_max_error_sign = True
            status_sign = True
        if rot_status[4][4] == 1:
            rot_max_error += f"W({error_rot[4][4]:.1f}%) "
            rot_max_error_sign = True
            status_sign = True

        if status_sign:
            status_info = Paragraph(u"&nbsp;&nbsp;&nbsp;&nbsp;<b>a. Overall Status: \
                                    <font color='red'>FAILED</font></b> ", styles['BodyText'])
        else:
            status_info = Paragraph(u"&nbsp;&nbsp;&nbsp;&nbsp;<b>a. Overall Status: \
                                    <font color='blue'>PASS</font></b> ", styles['BodyText'])

        # Build the PDF with the intro and tables
        elements = [title, Spacer(1, 20), info_title, Spacer(1, 5), first_info, Spacer(1, 20), result_title]

        trans_error_info = Paragraph("&nbsp;&nbsp;&nbsp;&nbsp<b>b. Translation Error</b>",
                                     styles['BodyText'])
        elements += [Spacer(1, 5), status_info, Spacer(1, 10), trans_error_info]

        if trans_rms_error_sign:
            trans_rms_error = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                                <b>i. RMS error exceeded the benchmark: </b>" + trans_rms_error
            trans_rms_error_info = Paragraph(trans_rms_error, styles['BodyText'])
            elements += [Spacer(1, 5), trans_rms_error_info]

        if trans_max_error_sign:
            trans_max_error = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                                <b>ii. Max error exceeded the benchmark: </b>" + trans_max_error
            trans_max_error_info = Paragraph(trans_max_error, styles['BodyText'])
            elements += [Spacer(1, 5), trans_max_error_info]

        rot_error_info = Paragraph("&nbsp;&nbsp;&nbsp;&nbsp<b>c. Rotation Error</b>",
                                   styles['BodyText'])
        elements += [Spacer(1, 5), rot_error_info]

        if rot_rms_error_sign:
            rot_rms_error = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                                <b>i. RMS error exceeded the benchmark: </b>" + rot_rms_error
            rot_rms_error_info = Paragraph(rot_rms_error, styles['BodyText'])
            elements += [Spacer(1, 5), rot_rms_error_info]

        if rot_max_error_sign:
            rot_max_error = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                                <b>ii. Max error exceeded the benchmark: </b>" + rot_max_error
            rot_max_error_info = Paragraph(rot_max_error, styles['BodyText'])
            elements += [Spacer(1, 5), rot_max_error_info]

        recommand_info = Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;<b>d. Recommandations: </b> ",
                                   styles['BodyText'])
        elements += [Spacer(1, 5), recommand_info]

        # Insert another page break for the next set of images
        elements.append(PageBreak())

        # Add torque and gain table
        elements += [sub_title, Spacer(1, 5)] + trans_table + [Spacer(1, 10)] + rot_table + [
            Spacer(1, 10)]

        elements.append(PageBreak())

        ############################### Error Plot ##################################
        elements += [plot_title]
        # Add first three images

        elements.append(Image(image_path[0], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[1], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[2], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))

        # Insert another page break for the next set of images
        elements.append(PageBreak())

        ############################### Task Space Tracking Plot ###############################
        elements += [task_title]

        elements.append(Image(image_path[18], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[19], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))

        elements.append(PageBreak())

        ################################### Torque Plot #######################################
        elements += [torque_plot_title]
        elements.append(Image(image_path[3], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[4], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[5], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))

        elements.append(PageBreak())

        ################################### Position Plot #####################################
        elements += [pos_title]

        elements.append(Image(image_path[6], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[7], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[8], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))

        elements.append(PageBreak())

        ################################### Velocity Plot #####################################
        elements += [vel_title]

        elements.append(Image(image_path[9], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[10], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[11], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))

        elements.append(PageBreak())

        ################################### Friction Plot #####################################
        elements += [fric_title]

        elements.append(Image(image_path[12], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[13], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path[14], width=480, height=180))  # Adjust width and height as needed
        elements.append(Spacer(1, 10))

        # Create a PDF document
        pdf = SimpleDocTemplate(pdf_path, pagesize=letter)
        pdf.build(elements, onFirstPage=self.addPageNumber, onLaterPages=self.addPageNumber)
