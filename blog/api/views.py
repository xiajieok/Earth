import os
from flask_restful import reqparse, abort, Api, Resource
from flask_moment import datetime
from blog import models
from flask import jsonify, request, render_template
from blog.ext import db
from blog.utils import auth
from blog.utils import get_dir

ansible_dir = get_dir('a_path')
playbook_dir = get_dir('play_book_path')

parser = reqparse.RequestParser()


class UserList(Resource):
    decorators = [auth.login_required]

    def get(self):
        user = models.User.query.all()
        res = {}
        for i in user:
            res[i.id] = {'username': i.username, 'email': i.email}
        return jsonify(res)

    def post(self):
        json_data = request.get_json(force=True)
        try:
            id = models.User.query.order_by(models.User.id.desc()).first().id
            new_id = int(id) + 1
        except:
            new_id = 1
        print('new_id', new_id)
        res = models.User(id=new_id, username=json_data['username'], email=json_data['email'],
                          password=json_data['password'])
        db.session.add(res)
        db.session.commit()
        db.session.close()
        return json_data, 200


class User(Resource):
    decorators = [auth.login_required]

    def get(self, user_id):
        user = models.User.query.filter_by(id=user_id)
        res = {}
        for i in user:
            res[i.id] = {'username': i.username, 'email': i.email}
        return jsonify(res)

    def put(self, user_id):
        json_data = request.get_json(force=True)
        for i in json_data:
            models.User.query.filter_by(id=user_id).update({i: json_data[i]})
        db.session.commit()
        db.session.close()
        return 200

    def delete(self, user_id):
        try:
            user = models.User.query.filter_by(id=user_id).delete()
            db.session.commit()
            db.session.close()
        except:
            return "Not exists"
        return 200


class IDCList(Resource):
    decorators = [auth.login_required]

    def get(self):
        idc = models.IDC.query.all()
        res = {}
        for i in idc:
            res[i.id] = {'name': i.name, 'memo': i.memo}
        return jsonify(res)

    def post(self):
        json_data = request.get_json(force=True)
        try:
            idc_id = models.IDC.query.order_by(models.IDC.id.desc()).first().id
            new_id = int(idc_id) + 1
        except:
            new_id = 1
        print(new_id)
        res = models.IDC(id=new_id, name=json_data['name'], memo=json_data['memo'])
        db.session.add(res)
        db.session.commit()
        db.session.close()
        return json_data, 200


class IDC(Resource):
    decorators = [auth.login_required]

    def get(self, idc_id):
        idc = models.IDC.query.filter_by(id=idc_id)
        res = {}
        for i in idc:
            res[i.id] = {'name': i.name, 'memo': i.memo}
        return jsonify(res)

    def put(self, idc_id):
        json_data = request.get_json(force=True)
        for i in json_data:
            models.IDC.query.filter_by(id=idc_id).update({i: json_data[i]})
        db.session.commit()
        db.session.close()
        return 200

    def delete(self, idc_id):
        try:
            idc = models.IDC.query.filter_by(id=idc_id).delete()
            print(idc)
            db.session.commit()
            db.session.close()
        except:
            return "Not exists"
        return 200


class BusinessUnitList(Resource):
    decorators = [auth.login_required]

    def get(self):
        business = models.BusinessUnit.query.all()
        res = {}
        for i in business:
            res[i.id] = {'name': i.name, 'memo': i.memo}
        return jsonify(res)

    def post(self):
        json_data = request.get_json(force=True)
        try:
            business_id = models.BusinessUnit.query.order_by(models.BusinessUnit.id.desc()).first().id
            new_id = int(business_id) + 1
        except:
            new_id = 1
        print(new_id)
        res = models.BusinessUnit(id=new_id, name=json_data['name'], memo=json_data['memo'])
        db.session.add(res)
        db.session.commit()
        db.session.close()
        return json_data, 200


class BusinessUnit(Resource):
    decorators = [auth.login_required]

    def get(self, business_id):
        business = models.BusinessUnit.query.filter_by(id=business_id)
        res = {}
        for i in business:
            res[i.id] = {'name': i.name, 'memo': i.memo}
        return jsonify(res)

    def put(self, business_id):
        json_data = request.get_json(force=True)
        for i in json_data:
            models.BusinessUnit.query.filter_by(id=business_id).update({i: json_data[i]})
        db.session.commit()
        db.session.close()
        return 200

    def delete(self, business_id):
        try:
            idc = models.BusinessUnit.query.filter_by(id=business_id).delete()
            print(idc)
            db.session.commit()
            db.session.close()
        except:
            return "Not exists"
        return 200


class blogList(Resource):
    decorators = [auth.login_required]

    def get(self):
        # print(request.args)

        try:
            data = request.args.to_dict()
            for k, v in data.items():
                if k == 'idc':
                    blog = models.blog.query.filter_by(idc=v)
                elif k == 'business_unit':
                    blog = models.blog.query.filter_by(business_unit=v)
                else:
                    blog = models.blog.query.filter_by(type=v)
            res = {}
            for i in blog:
                res[i.id] = {'hostname': i.hostname, 'type': i.type, 'sn': i.sn, 'ip': i.ip,
                             'model': i.model, "cpu_processor": i.cpu_processor, "cpu_model": i.cpu_model,
                             "cpu_num": i.cpu_num, "vendor": i.vendor, "os": i.os,
                             "cpu_physical": i.cpu_physical, "disk": i.disk, "memory": i.memory,
                             'status': i.status, 'idc': i.idc, 'business_unit': i.business_unit,
                             'expire_date': i.expire_date, 'create_date': i.create_date,
                             'update_date': i.update_date,
                             'approved': i.approved, 'memo': i.memo}

            return jsonify(res)
        except:
            blog = models.blog.query.all()
            res = {}
            for i in blog:
                res[i.id] = {'hostname': i.hostname, 'type': i.type, 'sn': i.sn, 'ip': i.ip,
                             'model': i.model, "cpu_processor": i.cpu_processor, "cpu_model": i.cpu_model,
                             "cpu_num": i.cpu_num, "vendor": i.vendor, "os": i.os,
                             "cpu_physical": i.cpu_physical, "disk": i.disk, "memory": i.memory,
                             'status': i.status, 'idc': i.idc, 'business_unit': i.business_unit,
                             'expire_date': i.expire_date, 'create_date': i.create_date,
                             'update_date': i.update_date,
                             'approved': i.approved, 'memo': i.memo}

            return jsonify(res)

    def post(self):
        json_data = request.get_json(force=True)
        print('提交到的数据', json_data)
        try:
            blog_id = models.blog.query.order_by(models.blog.id.desc()).first().id
            new_id = int(blog_id) + 1
        except:
            new_id = 1
        res = models.blog(id=new_id, hostname=json_data['hostname'], sn=json_data['sn'], type=json_data['type'],
                           os=json_data['os'], vendor=json_data['vendor'],
                           model=json_data['model'], cpu_processor=json_data['cpu_processor'],
                           cpu_model=json_data['cpu_model'],
                           cpu_num=json_data['cpu_num'], cpu_physical=json_data['cpu_physical'],
                           memory=json_data['memory'], disk=json_data['disk'],
                           idc=json_data['idc'], create_date=datetime.now(), update_date=datetime.now(),
                           status=json_data['status'])
        db.session.add(res)
        db.session.commit()
        db.session.close()
        return json_data, 200


class blog(Resource):
    decorators = [auth.login_required]

    def get(self, blog_id):
        blog = models.blog.query.filter_by(id=blog_id).first()
        res = {}
        res[blog.id] = {'hostname': blog.hostname, 'type': blog.type, 'sn': blog.sn, 'model': blog.model,
                         'ip': blog.ip, "cpu_processor": blog.cpu_processor, "cpu_model": blog.cpu_model,
                         "cpu_num": blog.cpu_num, "os": blog.os, "vendor": blog.vendor,
                         "cpu_physical": blog.cpu_physical, "disk": blog.disk, "memory": blog.memory,
                         'status': blog.status, 'idc': blog.idc, 'business_unit': blog.business_unit,
                         'expire_date': blog.expire_date, 'create_date': blog.create_date,
                         'update_date': blog.update_date,
                         'approved': blog.approved, 'memo': blog.memo}

        return jsonify(res)

    def put(self, blog_id):
        json_data = request.get_json(force=True)
        print('更新操作')
        for i in json_data:
            models.blog.query.filter_by(id=blog_id).update({i: json_data[i], "update_date": datetime.now()})
        db.session.commit()
        db.session.close()
        return 200

    def delete(self, blog_id):
        try:
            blog = models.blog.query.filter_by(id=blog_id).delete()
            print(blog)
            db.session.commit()
            db.session.close()
        except:
            return "Not exists"
        return 200


class Ansible(Resource):
    def get(self):
        # 获取yaml文件
        playbook_dir = get_dir('play_book_path')
        list = os.listdir(playbook_dir)
        books = {}
        for i in list:
            name = i[:-4]
            value = i
            books[name] = value
        return jsonify(books)

    def post(self):
        # 根据获取到 主机名/playbook 执行操作
        json_data = request.get_json(force=True)
        print('提交到的数据', json_data)
        print(json_data['hostname'])
        desc = models.blog.query.filter_by(hostname=json_data['hostname']).first()
        print(desc.ip)
        ansible = AnsibleApi()
        test = playbook_dir + 'test.yml'
        try:
            s = ansible.playbookrun(playbook_path=[test])
            print(s)
        except:
            return 500
        return 200
