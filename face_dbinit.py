# coding = utf-8
import sqlite3
import base64
import os
from reduce import *


def init_db():
    if os.path.exists("sys_db"):  # 判断数据库是否存在
        pass
    else:
        sql = sqlite3.connect("sys_db.db")  # 建立数据库连接
        cur = sql.cursor()  # 得到游标对象
        # 创建表
        cur.executescript("""
            create table if not exists staff_tb(
                id int not null primary key,
                sname varchar(40) not null ,
                department varchar(40) not null
            );
            create table if not exists logcat_tb(
            id int not null references staff_tb(id) ON DELETE CASCADE ON UPDATE CASCADE,
            clcokdate text not null,
            clocktime text not null,
            latetime text not null,
            primary key (id,clocktime)
        );
            create table if not exists admin_tb(
            id int not null primary key,
            adname varchar(40) not null,
            password varchar(30) not null
        );
            create table if not exists face_tb(
            id int not null primary key references staff_tb(id) ON DELETE CASCADE ON UPDATE CASCADE,
            facearray array not null
        );
        """)
        cur.close()
        sql.commit()
        sql.close()


def insert_staff(id, name, depart):
    sql = sqlite3.connect("sys_db.db")
    cur = sql.cursor()
    cur.execute("insert into staff_tb(id,sname,department) values (?,?,?)", (id, name, depart))
    cur.close()
    sql.commit()
    sql.close()


def insert_admin(id, name, passwd):
    passwd_bs64 = base64.b64encode(passwd.encode("utf-8"))
    sql = sqlite3.connect("sys_db.db")
    cur = sql.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")  # 开启外键约束
    cur.execute("insert into admin_tb(id,adname,password) values (?,?,?)", (id, name, passwd_bs64))
    cur.close()
    sql.commit()
    sql.close()


def insert_logcat(id, date, times, late):
    sql = sqlite3.connect("sys_db.db")
    cur = sql.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("insert into logcat_tb(id,clcokdate,clocktime,latetime) values (?,?,?,?)", (id, date, times, late))
    cur.close()
    sql.commit()
    sql.close()


def insert_face(id, face):
    sql = sqlite3.connect("sys_db.db")
    cur = sql.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("insert into face_tb(id,facearray) values (?,?)", (id, reduce_data(face)))
    cur.close()
    sql.commit()
    sql.close()


def load_admin(id, passwd):
    passwd_bs64 = base64.b64encode(passwd.encode("utf-8"))
    sql = sqlite3.connect("sys_db.db")
    cur = sql.cursor()
    cur.execute("select id,adname,password from admin_tb where id = (?) and password = (?)", (id, passwd_bs64))
    result = cur.fetchone()
    if result:
        cur.close()
        sql.close()
        return result[1]
    else:
        cur.close()
        sql.close()
        print("用户名或密码错误")


def load_face():
    face_data = [[], [], []]
    sql = sqlite3.connect("sys_db.db")
    cur = sql.cursor()
    cur.execute("select tb1.id,tb1.facearray,tb2.sname from face_tb as tb1 left join staff_tb as tb2 on tb1.id = tb2.id")
    results = cur.fetchall()
    for row in results:
        face_data[0].append(row[0])
        face_data[1].append(decompress_data(row[1])["arr_0"])
        face_data[2].append(row[2])
    return face_data


def load_logcat():
    sql = sqlite3.connect("sys_db.db")
    cur = sql.cursor()
    cur.execute("select tb1.id,tb1.sname,tb2.clcokdate,tb2.clocktime,tb2.latetime from \
             staff_tb as tb1 join logcat_tb as tb2 on tb1.id = tb2.id ")
    results = cur.fetchall()
    return results


def delete_data(id):
    sql = sqlite3.connect("sys_db.db")
    cur = sql.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("delete from staff_tb where id =(?)", (id,))
    cur.close()
    sql.commit()
    sql.close()


if __name__ == '__main__':
    init_db()
    load_face()
    # load_info(1223)
