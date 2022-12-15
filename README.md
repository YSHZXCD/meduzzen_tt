# Как использовать API

### Технологии:
- ```Python3``` - Programming language
- ```MongoDB``` - Database
- ```PyJWT``` - JWT token
- ```Flask``` - API
- ```Black``` - prettier
----

#### Создание админа и менеджера:

```$ flask create-admin <admin_name> <admin_password> <admin_phone_number>```<br>
```$ flask create-manager <manager_name> <manager_password> <manager_phone_number>```

#### Авторизация админа или менеджера идет через ```/login```

#### Method GET
```json
{
  "name": "admin",
  "password": "admin"
}
```

###### После успешной авторизации, пользователь получает токен.
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoidGVzdGluZyIsInBhc3N3b3JkIjoiYTY2NWE0NTkyMDQyMmY5ZDQxN2U0ODY3ZWZkYzRmYjhhMDRhMWYzZmZmMWZhMDdlOTk4ZTg2ZjdmN2EyN2FlMyJ9.hlyXKJjP-DInZwsai3FydRhYQkOUkLHaYrwEAuOjsMk"
}
```

---

# Location
#### Method: POST
```/location/add_location - Создание рабочей локации (может только менеджер)```
#### Request to send:
```json
{
  "location_name": "location1"
}
```

#### Response:
```json
{
    "_id": "639a3261eb28678fadd55711",
    "emp_on_location": "None",
    "location_name": "location1"
}
```
----
#### Method: POST
```/location/add_emp_to_location/<worker_id>/<location_id> - Добавить работника на локацию (может только менеджер)```
#### Request to send:
#### Response
```json
{
    "_id": "639a3261eb28678fadd55711",
    "emp_on_location": "639a379850bfa9f4c0fd7634",
    "location_name": "location1"
}
```
----
#### Method DELETE
```/location/remove_emp_location/<worker_id>```
#### Response
```json
{
    "status": "Location is clear"
}
```

-------
# Employee (Worker)
#### Method POST
```/emp/create_employee - Создать работника (может только менеджер)```
```json
{
    "name": "Yevhenii",
    "speciality": "Hairdresser",
    "phone_number": "+38098791107",
    "email": "hairdresser123321@gmail.com"
}
```

#### Response:
```json
{
    "_id": "639a33afeb28678fadd55712",
    "appointments": [],
    "email": "hairdresser123321@gmail.com",
    "location": "None",
    "name": "Yevhenii",
    "phone_number": "+38098791107",
    "schedule": {},
    "speciality": "Hairdresser"
}
```
----
#### Method DELETE
```/emp/remove_employee/<worker_id> - Удалить работника (может только менеджер)```
#### Response
```json
{
    "status": "Employee has been deleted"
}
```
----
#### Method POST
```/emp/set_schedule/<worker_id> - Добавить график работы (может только менеджер)```
#### Request to send:
```json
{
    "work_time": {
        "25.04.2024": ["10:00-12:00", "16:00-20:00"],
        "24.04.2024": ["10:00-12:00", "16:00-20:00"]
    }
}
``` 
#### Response
```json
{
    "_id": "639a379850bfa9f4c0fd7634",
    "appointments": [],
    "email": "hairdresser123321@gmail.com",
    "location": "None",
    "name": "Yevhenii",
    "phone_number": "+38098791107",
    "schedule": {
        "25.04.2024": {
            "0": "10:30-12:30",
            "1": "15:00-20:00"
        }
    },
    "speciality": "Hairdresser"
}
```
----
#### Method GET
```/emp/get_emp_schedule/<worker_id> - Посмотреть график работы (может только менеджер)```
#### Response
```json
{
    "schedule": {
        "25.04.2024": {
            "0": "10:30-12:30",
            "1": "15:00-20:00"
        }
    }
}
```
----

# Groups
#### Method POST
```/group/create_group - Создать группу (может только администратор)```
#### Request to send
```json
{
    "group_name": "Test group"
}
```

#### Response
```json
{
    "_id": "639a3b81e9367610c1fc4c94",
    "group_name": "Test group",
    "users": []
}
```
----
#### Method DELETE
```/remove_group/<group_id> - Удалить группу (может только администратор)```
#### Response
```json
{
  "status": "Group has been deleted"
}
```
----
#### Method DELETE
```/group/remove_user/<group_id>/<user_id> - Удалить пользователя или работника из группы (может только менеджер)```
#### Response
```json
{
    "_id": "639929faef6a1a75f82ddfdc",
    "group_name": "Test group",
    "users": []
}
```
----
#### Method POST
```/group/add_user/<group_id>/<user_id> - Добавить пользователя или работника в группу (может только администратор)```
#### Response
```json
{
    "_id": "639929faef6a1a75f82ddfdc",
    "group_name": "manager",
    "users": [
        {
            "_id": "639929faef6a1a75f82ddfdb",
            "name": "manager",
            "phone_number": "1234"
        }
    ]
}
```
----

# User
#### Method POST
```/ - Создать пользователя (может только администратор)```
#### Request to send
```json
{
    "name": "testing",
    "password": "123",
    "phone_number": "09879123123"
}
```
#### Response
```json
{
    "_id": "639a400b0747caca0e2aaab3",
    "name": "testing",
    "phone_number": "09879123123"
}
```
---
#### Methods GET
```/login - Логин пользователя```
#### Request to send
```json
{
  "name": "login",
  "password": "password"
}
```
#### Response
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoidGVzdGluZyIsInBhc3N3b3JkIjoiYTY2NWE0NTkyMDQyMmY5ZDQxN2U0ODY3ZWZkYzRmYjhhMDRhMWYzZmZmMWZhMDdlOTk4ZTg2ZjdmN2EyN2FlMyJ9.hlyXKJjP-DInZwsai3FydRhYQkOUkLHaYrwEAuOjsMk"
}
```
----
#### Method GET
```/get_emp - Посмотреть список всех работников (могут все в открытом доступе)```<br>
У данного эндпоинта есть аргументы сортировки: speciality и date<br>
```/get_emp/?speciality=hairdresser - Вывод всех парикмахеров```<br>
```/get_emp/?date=25.03.2023 - Вывод всех сотрудников у которых есть время в данный день```
#### Response
```json
{
    "employees": [
        {
            "_id": "639a7eff9274a59edb3b72de",
            "appointments": [],
            "email": "hairdresser@gmail.com",
            "location": "None",
            "name": "test1",
            "phone_number": "12312312",
            "schedule": {
                "work_time": {
                    "24.04.2024": [
                        "10:00-12:00",
                        "16:00-20:00"
                    ],
                    "25.04.2024": [
                        "10:00-12:00",
                        "16:00-20:00"
                    ]
                }
            },
            "speciality": "hairdresser"
        }
    ]
}
```
----
#### Method POST
```/create_appointment/<worker_id> - Создать запись для работника (может только администратор)```
#### Request to send
```json
{
    "client_description": {
        "name": "Daria",
        "surname": "P.",
        "phone_number": "3809897123"
    },
    "date": "25.04.2024",
    "start": "10:30",
    "end": "12:30"
}
```
#### Response
```json
{
    "_id": "639a379850bfa9f4c0fd7634",
    "appointments": [
        "639a43feb600d0a00c6c4bbc"
    ],
    "email": "hairdresser123321@gmail.com",
    "location": "None",
    "name": "Yevhenii",
    "phone_number": "+38098791107",
    "schedule": {
        "25.04.2024": {
            "0": "10:30-12:30",
            "1": "15:00-20:00"
        }
    },
    "speciality": "Hairdresser"
}
```