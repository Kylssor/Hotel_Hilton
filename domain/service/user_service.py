# domain/service/user_service.py
class UserService:
    def get_cliente_profile(self, usuario):
        return {
            "message": "Bienvenido cliente",
            "usuario_id": usuario["id"]
        }

    def get_empleado_profile(self, usuario):
        return {
            "message": "Bienvenido empleado",
            "usuario_id": usuario["id"]
        }
