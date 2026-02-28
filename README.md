# Practical lesson pz-MQTT  
# Розгортання та налаштування MQTT-брокера  

> У цьому занятті студенти отримують практичні навички роботи з MQTT-брокером.  
> Мета — навчитися розгортати брокер,та обмін повідомленнями за допомогою публікації/підписки.

---

## What need to do:
* Розгорнути MQTT-брокер (Mosquitto / EMQX / HiveMQ)
* Налаштувати базову конфігурацію сервісу  
* Ознайомитись із принципами роботи MQTT-протоколу  
* Виконати публікацію та підписку на MQTT-топіки через Postman або інший MQTT-клієнт  
* Перевірити працездатність сервісу через інструменти тестування  

---

## Acceptance criteria
* Студент розгорнув MQTT-брокер або локально / у Docker  
* Мінімальна конфігурація працює стабільно  
* Студент розуміє основні поняття MQTT:
  * Topic  
  * Publish  
  * Subscribe  
  * QoS  
* Виконано демонстрацію Publish/Subscribe через Postman або інший клієнт  
* Усі команди, налаштування та тести описані в README.md  
* Надано скріншоти або лог дії Publish/Subscribe (за потреби)  
* Завдання оформлене відповідно до структури проєкту  

---

## Getting started


```bash
docker compose up

```

```
├── stt-pz-3
│   ├── broker
│   │   ├── <mqtt>.conf     # конфігурація MQTT (якщо застосовується)
│   │   ├── docker-compose.yml # варіант розгортання брокера
│   ├── screenshots            # докази роботи Publish/Subscribe або Gateway routes
│   ├── .editorconfig
│   ├── .gitignore
│   ├── README.md
└──

```
## Usfull links

[MQTT Essentials](https://www.hivemq.com/mqtt-essentials/)

[EMQX Documentation](https://www.emqx.io/docs/en/latest/)

[Eclipse Mosquitto](https://mosquitto.org/)

[MQTT with Postman](https://learning.postman.com/docs/sending-mqtt-messages/intro-to-mqtt/)

[NGINX API Gateway](https://docs.nginx.com/nginx/admin-guide/api-gateway/)
