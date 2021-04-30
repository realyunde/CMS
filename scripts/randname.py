import random
import hashlib


def make_token(password):
    salt = b'cms_token'
    if isinstance(password, str):
        password = password.encode('utf-8')
    md5 = hashlib.md5(salt + password)
    return md5.hexdigest()


lastname = '赵钱孙李周吴郑王' \
           '冯陈卫蒋沈韩杨毛' \
           '朱秦尤许何吕施张' \
           '孔曹严华金魏陶姜' \
           '戚谢邹喻水云苏潘' \
           '范彭韦昌马方任袁' \
           '柳鲍史唐费岑薛雷' \
           '贺倪汤滕殷罗毕郝' \
           '齐康伍余元顾孟黄' \
           '和穆萧尹姚邵湛汪' \
           '舒屈项祝董粱杜阮' \
           '席季麻强贾路娄危' \
           '江童颜郭梅牛林丁' \
           '钟徐邱高夏蔡田邓' \
           '胡凌霍万柯卢莫房' \
           '郁单杭洪包诸左石' \
           '崔龚程邢裴陆文习' \
           '靳邴松井富乌焦曾' \
           '山谷车侯伊宁仇祖' \
           '武符刘詹龙叶尚农' \
           '司黎乔温瞿耿关红'

female = '秀娟英华慧巧美娜' \
         '静淑惠珠翠雅芝玉' \
         '萍红娥玲芬芳燕彩' \
         '春菊兰凤洁梅琳素' \
         '云莲真环雪荣爱妹' \
         '霞香月莺媛艳瑞凡' \
         '佳嘉琼勤珍贞莉桂' \
         '娣叶璧璐娅琦晶妍' \
         '茜秋珊莎锦黛青倩' \
         '婷姣婉娴瑾颖露瑶' \
         '怡婵雁蓓纨仪荷丹' \
         '蓉眉君琴蕊薇菁梦' \
         '岚苑婕馨瑗琰韵融' \
         '园艺咏卿聪澜纯毓' \
         '悦昭冰爽琬茗羽希' \
         '宁欣飘育滢馥筠柔' \
         '竹霭凝晓欢霄枫芸' \
         '菲寒伊亚宜可姬舒' \
         '影荔枝思丽'

male = '伟刚勇毅俊峰强军' \
       '平保东文辉力明永' \
       '健世广志义兴良海' \
       '山仁波宁贵福生龙' \
       '元全国胜学祥才发' \
       '武新利清飞彬富顺' \
       '信子杰涛昌成康星' \
       '光天达安岩中茂进' \
       '林有坚和彪博诚先' \
       '敬震振壮会思群豪' \
       '心邦承乐绍功松善' \
       '厚庆磊民友裕河哲' \
       '江超浩亮政谦亨奇' \
       '固之轮翰朗伯宏言' \
       '若鸣朋斌梁栋维启' \
       '克伦翔旭鹏泽晨辰' \
       '士以建家致树炎德' \
       '行时泰盛雄琛钧冠' \
       '策腾楠榕风航弘'


def random_key(teacher):
    if teacher:
        key = '{:0>2}'.format(str(random.randint(1, 20)))
        key += '{:0>4}'.format(str(random.randint(0, 9999)))
    else:
        key = '{:0>4}'.format(str(random.randint(2000, 2020)))
        key += '{:0>4}'.format(str(random.randint(0, 9999)))
        key += '{:0>4}'.format(str(random.randint(0, 9999)))
    return key


def random_name():
    name = lastname[random.choice(range(len(lastname)))]
    if random.choice(range(2)):
        name += female[random.choice(range(len(female)))]
    else:
        name += male[random.choice(range(len(male)))]
    return name


def main():
    items = {}
    for i in range(50):
        while True:
            key = random_key(True)
            if key not in items:
                break
        name = random_name()
        items[key] = name
    sql = "INSERT INTO `table` (`id`, `name`, `token`) VALUES\n"
    for key in items:
        sql += "('{}', '{}', '{}'), \n".format(key, items[key], make_token(key))
    print(sql)


if __name__ == '__main__':
    main()
