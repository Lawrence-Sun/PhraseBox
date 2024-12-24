import pandas as pd


# 读取文本文件的生成器
def read_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()

def convert_to_csv(fileName, outputName):
    # 初始化变量
    data_list = []
    id_value = ''
    link = ''
    description = ''
    patient = ''
    doctor = ''
    patient_flag = False
    doctor_flag = False

    # name = 'healthcaremagic_dialogue_4'
    name = fileName

    # 创建一个迭代器
    # lines = read_file(f'{name}.txt')
    lines = read_file(fileName)
    line = next(lines, None)

    # 解析文本文件内容
    while line is not None:
        if line.startswith('id='):
            if id_value:  # 如果已经有数据，说明是一组新的数据
                data_list.append({
                    'id': id_value,
                    'link': link,
                    'description': description,
                    'patient': patient.strip(),
                    'doctor': doctor.strip()
                })
                # 重置变量
                id_value = ''
                link = ''
                description = ''
                patient = ''
                doctor = ''
                patient_flag = False
                doctor_flag = False
            id_value = line.split('=')[1]
        elif line.startswith('http'):
            link = line
        elif line.startswith('Description'):
            description = next(lines, '').strip()
        elif line.startswith('Patient:'):
            patient_flag = True
            doctor_flag = False
            patient = ''
        elif line.startswith('Doctor:'):
            doctor_flag = True
            patient_flag = False
            doctor = ''
        elif patient_flag:
            if line.startswith('Doctor:'):
                patient_flag = False
                doctor_flag = True
                doctor = ''
            else:
                patient += line + ' '
        elif doctor_flag:
            if line == '':
                doctor_flag = False
            else:
                doctor += line + ' '
        
        line = next(lines, None)

    # 添加最后一组数据
    if id_value:
        data_list.append({
            'id': id_value,
            'link': link,
            'description': description,
            'patient': patient.strip(),
            'doctor': doctor.strip()
        })

    # 创建一个DataFrame
    df = pd.DataFrame(data_list)

    # 将DataFrame写入到CSV文件
    # csv_file_path = f'{name}.csv'
    # df.to_csv(csv_file_path, index=False)

    df.to_csv(outputName, index=False, encoding='utf-8')

    # 显示结果
    print(df)