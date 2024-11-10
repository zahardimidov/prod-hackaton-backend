from config import ADMIN_PASSWORD, ADMIN_USERNAME
from database.models import Bill, BillMember, Group, GroupMember, Product, User
from fastapi import Request
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        if not (username == ADMIN_USERNAME and password == ADMIN_PASSWORD):
            return False

        request.session.update(
            {"token": "fdbb0dd1-a368-4689-bd71-5888f69b438e"})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token == 'fdbb0dd1-a368-4689-bd71-5888f69b438e':
            return False
        return True


authentication_backend = AdminAuth(secret_key="secret")


class UserAdmin(ModelView, model=User):
    column_list = [User.username, User.id]

    can_create = False
    can_edit = True
    form_widget_args_update = dict(
        id=dict(readonly=True), username=dict(readonly=True))


class GroupAdmin(ModelView, model=Group):
    column_list = [Group.title, Group.single, Group.id]


class BillAdmin(ModelView, model=Bill):
    column_list = [Bill.title, Bill.group]


class BillMemberAdmin(ModelView, model=BillMember):
    column_list = [BillMember.bill, BillMember.member,
                   BillMember.money, BillMember.paid_dolg, BillMember.dolg]


class GroupMemberAdmin(ModelView, model=GroupMember):
    column_list = [GroupMember.member, GroupMember.group]


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.name, Product.price, Product.quantity, Product.bill]


def init_admin(app, engine):
    admin = Admin(app, engine=engine,
                  authentication_backend=authentication_backend)
    admin.add_view(UserAdmin)
    admin.add_view(GroupAdmin)
    admin.add_view(GroupMemberAdmin)
    admin.add_view(BillAdmin)
    admin.add_view(BillMemberAdmin)
    admin.add_view(ProductAdmin)
