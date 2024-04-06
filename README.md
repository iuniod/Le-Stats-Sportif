Nume: Iustina-Andreea Cărămidă
Grupă:

# Tema 1 - Le Stats Sportif

Organizare
-
***Explicație pentru soluția aleasă:*** 

* Am ales pentru această temă să implementez clasa ThreadPool în loc să o folosesc pe cea predefinită pentru a putea spune că am folosit mecanisme de sincronizare în cod (un lock și o variabilă de condiție).

* Am ales să implementez clasa Job pentru a organiza mai bine codul și a face diferențierea dintre cele 3 zone de cod mai bună (citirea: funcțiile API-urilor, procesarea: calcularea statisticilor bazăndu-ne pe API-ul care a creat jobul și programarea thread-urilor: adăugarea job-urilor în coadă și așteptarea terminării lor).
```
class Job:  # pylint: disable=too-few-public-methods
    def __init__(self, job_id, input_data, command, logger):
        self.job_id = job_id # id ul jobului
        self.input_data = input_data # json-ul primit de la client cu datele de intrare
        self.status = "running" # statusul jobului - când este creat este running deoaerece intră automat în coadă
        self.command = command # tipul API-ului care a creat jobul
        self.logger = logger # logger-ul pentru debug
```

* Am ales să scriu o funcție generică pentru majoritatea API-urilor de tipul POST pentru a nu avea cod duplicat.

```
def send_job_to_thread_pool(req, api_endpoint):
    """ Send the job to the thread pool for processing """
    # Check if ThreadPool is still accepting jobs
    if not webserver.tasks_runner.accepting_jobs:
        return jsonify({
            "status": "error",
            "reason": "Server is shutting down"
        })

    # Get request data
    data = req.json

    # Register job. Don't wait for task to finish
    job_id = webserver.job_counter
    webserver.tasks_runner.register_job(job_id, data, api_endpoint)

    # Increment job_id counter
    webserver.job_counter += 1

    # Return associated job_id
    return jsonify({"job_id": "job_id_" + str(job_id)})
```

* Am implementat câte un fișier unit test pentru fiecare modul din cod pentru a testa funcționalitățile acestora separat.
```
- unittests/
	- data_ingestion_unittest.py
	- routes_unittest.py
	- thread_pool_unittest.py
```

* Inițial, am vrut să stochez rezultatul fiecărui job într-o variabilă din clasă, dar mi-am dat seama că acest lucru deși ar aduce un plus de rapiditate pentru API-ul /api/get_result/<job_id>, ar aduce un minus destul de semnificativ pe partea de memorie, deoarece rezultatele ar fi stocate în memorie de 2 ori: o dată în fișierele fiecărui job și o dată în variabila din clasă.

* Deși scopul inițial al temei probabil era să învățăm metode de sincronizare în python, consider că tema a fost utilă pentru a învăța cum să facem un server web în python, cum să folosim API-uri, cum să facem teste unitare în python și cum să folosim fișierele de tip log.

* Implementarea este eficientă pentru că am folosit mecanisme de sincronizare, am folosit un logger pentru a scrie mesaje de debug și codul este organizat în clase și funcții.


***Cazuri speciale:***
* Am ales să creez un caz special pentru API-ul /api/graceful_shutdown când serverul deja a mai primit un mesaj de shutdown. În acest caz, serverul va returna un json:
```
{
	"status": "error",
	"reason": "Server is already shutting down"
}
```

* De asemenea, de ficare dată după un semnal de shutdown, dacă se mai încearcă primirea unui job, serverul va returna:
```
{
	"status": "error",
	"reason": "Server is shutting down"
}
```


Implementare
-

* Toate API-urile sunt implementate în fișierul routes.py, toate testele sunt in folderul unittests, fișierele de log sunt în folderul logs, folderul git atestă faptul că am folosit git.

* Nu am implementări extra ale temei.

* Nu am întâlnit dificultăți pe parcurs în afara dificultății de a mă motiva să termin tema cât mai devreme, pentru a nu o lăsa pe ultima sută de metrii ca în alți ani.


Resurse utilizate
-

* [How to use log files in Python](https://docs.python.org/3/howto/logging.html)
* [How to write unittests in Python](https://docs.python.org/3/library/unittest.html)
* [Mocking in Python](https://www.fugue.co/blog/2016-02-11-python-mocking-101)

Git
-
* [Repo privat Github](git@github.com:iuniod/Le-Stats-Sportif.git)
