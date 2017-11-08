# CthCoin
A web/crypto CTF Challenge for the Hack.lu 2016


- Title: CthCoin

- Text: Cthulhu awakens and all worshippers will be rewarded greatly! A new Cryptocurrency was created, and Cthulhu generous gives away free coins. Can you break it, but be careful do not provoke him.

- Points: 150

- [Dowload]()

- Solution: You need 120 to buy the flag but only get 65. Check /robots.txt to find /debugcoins. The coin is md5ed when spending it. To perform double spending you need to alter the coin so you get a different md5 hash. As everything is signed only the signature can be altered. Signature algo is ECDSA, ECDSA is Malleable (in bitcoin known as Transaction Malleability). So for signature (r,s), the signature (r, -s (mod N)) is valid. The curve is public and inside the coin. Check watchdog.py for code.

---

# Setup

- create virtual env (python3 virtualenv3)
	`virtualenv venv`

- activate it
	`source venv/bin/activate`

- install requirements
	`pip install -r requirements.txt`

- create a new sk.pem
	`python genkey.py`

- create database
	`python createdb.py`

- run it
	`gunicorn -w 4 -b 0.0.0.0:80 ctfapp:app`

- or for debug
	`python run.py`

- watchdog/solution
	requirements.txt
	exit(1) on fail exit(0) on success
	should not be run every min as is takes quite some time

	`watchdog.py ip port`
