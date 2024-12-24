import pandas as pd

# 读取文本文件的生成器
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line.strip()

def convert_to_csv(fileName, outputName):

    # 初始化变量
    data_list = []
    id_value = ''
    link = ''
    doctor = ''
    patient = ''
    faculty = ''
    disease = ''
    description = ''
    treatment_history = ''
    help_needed = ''
    dialogue = []
    patient_flag = False
    doctor_flag = False

    dialogue_flag = False
    unLinked_patient = ''
    unLinked_doctor = ''
    writing_dialogue_flag = False

    # 创建一个迭代器
    lines = read_file(fileName)
    line = next(lines, None)

    # 解析文本文件内容
    while line is not None:
        # print(f"Processing line: {line}")  # 调试信息
        if line.startswith('id='):
            # print(f"Found id line: {line}")  # 调试信息
            if id_value:  # 如果已经有数据，说明是一组新的数据
                # print(f"Adding data for id={id_value}")
                # 检查是否有未补齐的对话
                if doctor_flag and patient_flag:
                    dialogue.append({'patient': patient.strip(), 'doctor': doctor.strip()})
                if patient_flag and not doctor_flag:
                    dialogue.append({'patient': patient.strip(), 'doctor': ''})
                elif doctor_flag and not patient_flag:
                    dialogue.append({'patient': '', 'doctor': doctor.strip()})
                for d in dialogue:
                    if d == dialogue[0]:
                        data_list.append({
                            'id': id_value,
                            'link': link,
                            'faculty': faculty,
                            'disease': disease,
                            'description': description,
                            'treatment_history': treatment_history,
                            'help_needed': help_needed,
                            'doctor': d['doctor'],
                            'patient': d['patient']
                        })
                    else:
                        data_list.append({
                            'id': id_value,
                            'link': link,
                            'faculty': '',
                            'disease': '',
                            'description': '',
                            'treatment_history': '',
                            'help_needed': '',
                            'doctor': d['doctor'],
                            'patient': d['patient']
                        })
                # 重置变量
                id_value = ''
                link = ''
                doctor = ''
                patient = ''
                faculty = ''
                disease = ''
                description = ''
                treatment_history = ''
                help_needed = ''
                dialogue = []
                patient_flag = False
                doctor_flag = False
            id_value = line.split('=')[1]
            # print(f"Set id_value to: {id_value}")  # 调试信息
        elif line.startswith('http'):
            link = line
            # print(f"Set link to: {link}")  # 调试信息
        elif line.startswith('Doctor faculty'):
            faculty = next(lines, '').strip()
            # print(f"Set faculty to: {faculty}")  # 调试信息
        elif line.startswith('疾病'):
            disease = line + next(lines, '').strip()
            # print(f"Set disease to: {disease}")  # 调试信息
        elif line.startswith('病情描述（发病时间、主要症状、就诊医院等）') or line.startswith('病情描述'):
            description = line + next(lines, '').strip()
            # print(f"Set description to: {description}")  # 调试信息
        elif line.startswith('曾经治疗情况和效果'):
            treatment_history = line + next(lines, '').strip()
            # print(f"Set treatment_history to: {treatment_history}")  # 调试信息
        elif line.startswith('想得到怎样的帮助') or line.startswith('希望提供的帮助') or line.startswith('希望获得的帮助'):
            help_needed = line + next(lines, '').strip()
            # print(f"Set help_needed to: {help_needed}")  # 调试信息

        elif line.startswith('医生：'):
            if doctor_flag and not patient_flag:
                dialogue.append({'patient': '', 'doctor': doctor.strip()})
                doctor = ''
             
            if doctor_flag and patient_flag:
                dialogue.append({'patient': patient.strip(), 'doctor': doctor.strip()})
                patient = ''
                doctor = ''

                patient_flag = False

            if not doctor_flag:
                doctor_flag = True

        elif line.startswith('病人：'):
            if patient_flag and not doctor_flag:
                dialogue.append({'patient': patient.strip(), 'doctor': ''})
                patient = ''
            
            if patient_flag and doctor_flag:
                dialogue.append({'patient': patient.strip(), 'doctor': doctor.strip()})
                patient = ''
                doctor = ''

                doctor_flag = False

            if not patient_flag:
                patient_flag = True
        
        elif doctor_flag and doctor == '':
            doctor += line + ' '
        
        elif patient_flag and patient == '':
            patient += line + ' '

        line = next(lines, None)

    # 添加最后一组数据
    if id_value:
        # print(f"Adding final data for id={id_value}")
        # 检查是否有未补齐的对话
        if doctor_flag and patient_flag:
            dialogue.append({'patient': patient.strip(), 'doctor': doctor.strip()})
        if patient_flag and not doctor_flag:
            dialogue.append({'patient': patient.strip(), 'doctor': ''})
        elif doctor_flag and not patient_flag:
            dialogue.append({'patient': '', 'doctor': doctor.strip()})
        for d in dialogue:
            data_list.append({
                'id': id_value,
                'link': link,
                'faculty': faculty,
                'disease': disease,
                'description': description,
                'treatment_history': treatment_history,
                'help_needed': help_needed,
                'doctor': d['doctor'],
                'patient': d['patient']
            })

    # 创建一个DataFrame
    df = pd.DataFrame(data_list)

    # 将DataFrame写入到CSV文件
    csv_file_path = '/Users/sunmingchen/../../Volumes/THEMATRIX/phraseBank/2011_utf8.csv'

    # 将DataFrame写入到CSV文件，使用不同的编码格式
    # df.to_csv(csv_file_path, index=False)
    # df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
    df.to_csv(outputName, index=False, encoding='utf-8')

    # 显示结果
    print(df)