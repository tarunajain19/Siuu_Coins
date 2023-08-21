from flask import Flask,render_template,redirect,request,session,url_for,message_flashed,flash,Response
import smtplib
import json
from eth_account import Account
import secrets
import requests
from etherscan import *
from web3 import Web3
import email.utils
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint
from http.client import HTTPResponse
import cx_Oracle
import pandas as pd
import numpy as np
import argparse

import hashlib
import os
import copy
from datetime import timedelta
import datetime
# from pydub import AudioSegment
# from pydub.playback import play

# from hand_counter import hand_tracker
# from virtual_painter import letter_recognition
from time import sleep
import math
import time
# import cv2
import os
# import cv2
import numpy as np
from datetime import datetime

import time

import random
import threading
# import * as bcrypt from 'bcrypt'
conn=cx_Oracle.connect('BlackRock/WIN@//localhost:1521/orcl')
cur=conn.cursor()
# cur.execute("CREATE TABLE  IF NOT EXISTS EDUKIDS (USERNAME VARCHAR2(20) PRIMARY KEY,FIRST VARCHAR2(20),SECOND VARCHAR(20),PASSWORD VARCHAR2(20),AGE NUMBER(2),GENDER VARCHAR2(20), EMAIL VARCHAR2(23))")
# conn.commit()
ethereum_node_url = "https://goerli.infura.io/v3/addeba16509f4dc9a20b3716aca61a6c"
web3 = Web3(Web3.HTTPProvider(ethereum_node_url))
app = Flask(__name__)
app.secret_key="super secret keyy"
# app.permanent_session_lifetime=timedelta(days=365)


# def timer():
#     global camera_on_time
#     camera_on_time = 0
    
#     while True:
#         time.sleep(60)
#         camera_on_time += 1


def encrpt(password):
    # salt=bcrypt.genSaltSync()
    # hashed=bcrypt.hash(password,salt)
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password
def verify(to_address):

    verify_code=str(randint(10000,99999))
    msg=MIMEMultipart()
    msg['to']=email.utils.formataddr(('Recipient',to_address))
    msg['from']=email.utils.formataddr(('SIUU COINS','tarunajain109@gmail.com'))
    msg['Subject']='Email Verification Code from Siuu Coins'
    body=f'Your verification code is {verify_code}.'
    msg.attach(MIMEText(body,'plain'))
    with smtplib.SMTP('smtp.gmail.com',587) as server:
        server.starttls()
        server.login('tarunajain109@gmail.com','rxuvvwejvbsashir')
        server.sendmail('tarunajain109@gmail.com',[to_address],msg.as_string())
    return verify_code  
def reset_pass(to_address):
    verify_code=str(randint(10000,99999))
    msg=MIMEMultipart()
    msg['to']=email.utils.formataddr(('Recipient',to_address))
    msg['from']=email.utils.formataddr(('Siuu Coins','tarunajain109@gmail.com'))
    msg['Subject']='Reset Password Code from Siuu coins'
    body=f'Your verification code is {verify_code}.'
    msg.attach(MIMEText(body,'plain'))
    with smtplib.SMTP('smtp.gmail.com',587) as server:
        server.starttls()
        server.login('tarunajain109@gmail.com','rxuvvwejvbsashir')
        server.sendmail('tarunajain109@gmail.com',[to_address],msg.as_string())
    return verify_code  


@app.route('/')
def hello_world():
    # cap=cv2.VideoCapture(0)
    # return render_template("letter_recog.html",msg='0')
    return render_template("index.html") # home page
@app.route('/dash')
def dash():
    return render_template("login.html")
@app.route('/removee')
def removee():
    # print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    if 'email' in session:
        PRODUCT_ID = request.args.get('variable')
        # print("hi")
        user_id=session['email']
        cur.execute("DELETE FROM CART WHERE PRODUCT_ID=:PRODUCT_ID and user_id=:user_id",{"PRODUCT_ID":PRODUCT_ID,"user_id":user_id})
        conn.commit()
        print("hi")
        return redirect(url_for('display'))
    return redirect(url_for('home'))  

@app.route('/home')
def home(): #dashboard
    # if 'username' in session:
        # z=letter_recongnition(1)
        # if z==0:
        #     print("hi")
        # else:
        #     print("oops")
        # hand_tracker()
    cur.execute("SELECT SNO, NAME FROM VARIETY")
    variety_data = cur.fetchall()

    variety_products = []
    # for sno, name in variety_data:
    #     cur.execute("SELECT PRODUCT_NAME, DESCRIPTION, PRICE FROM PRODUCTS WHERE VARIETY_ID = :sno", {"sno": sno})
    #     products = cur.fetchall()
    #     variety_products.append((name, products))

    # # cursor.close()
    # # print(variety_products)
    # return render_template('login.html',variety_products=variety_products)
    for sno, name in variety_data:
        cur.execute("SELECT PRODUCT_ID, PRODUCT_NAME, DESCRIPTION, PRICE FROM PRODUCTS WHERE VARIETY_ID = :sno", {"sno": sno})
        products = cur.fetchall()

        products_with_images = []
        for product in products:
            product_id = product[0]
            image_filename = f"static/images/{sno}/{product_id}.jpg"
            products_with_images.append((product[1], product[2], product[3], image_filename))

        variety_products.append((sno,name, products_with_images))
    return render_template('login.html', variety_products=variety_products)
@app.route('/cat')
def cat():
    sno = request.args.get('variable')
    # print(sno)
    
    cur.execute("SELECT  NAME FROM VARIETY WHERE SNO= :sno",{"sno":sno})
    xx = cur.fetchone()
    cur.execute("SELECT PRODUCT_ID, PRODUCT_NAME, DESCRIPTION, PRICE FROM PRODUCTS WHERE VARIETY_ID = :sno", {"sno": sno})
    products = cur.fetchall()
    variety_products = []
    products_with_images = []
    for product in products:
        product_id = product[0]
        image_filename = f"static/images/{sno}/{product_id}.jpg"
        products_with_images.append((product[1], product[2], product[3], image_filename,product[0]))

    variety_products.append((xx, products_with_images))
    return render_template('search1.html', variety_products=variety_products)

@app.route('/info')
def info():
    PRODUCT_ID = request.args.get('variable')
    cur.execute("SELECT VARIETY_ID, PRODUCT_NAME, DESCRIPTION, PRICE FROM PRODUCTS WHERE PRODUCT_ID = :PRODUCT_ID", {"PRODUCT_ID": PRODUCT_ID})
    products = cur.fetchall()
    variety_products = []
    products_with_images = []
    for product in products:
        VARIETY_ID = product[0]
        image_filename = f"static/images/{VARIETY_ID}/{PRODUCT_ID}.jpg"
        actual=math.ceil(product[3]*0.98)

       
        coin=product[3]*0.02/50
        # print(coin)
        products_with_images.append((product[1], product[2], product[3], image_filename,product[0],actual,coin,PRODUCT_ID))

    # variety_products.append((xx, products_with_images))
    return render_template('search2.html', variety_products=products_with_images)
@app.route('/display')
def display():
    if 'email' in session:
        user_id=session['email']
        cur.execute("SELECT PRODUCT_ID from Cart WHERE user_id = :user_id", {"user_id": user_id})
        product_ids = cur.fetchall()
        products_with_images = []
        total=0
        for product in product_ids:
            PRODUCT_ID=product[0]
            cur.execute("SELECT VARIETY_ID, PRODUCT_NAME, DESCRIPTION, PRICE FROM PRODUCTS WHERE PRODUCT_ID = :PRODUCT_ID", {"PRODUCT_ID": PRODUCT_ID})
            products = cur.fetchone()
            VARIETY_ID = products[0]
            image_filename = f"static/images/{VARIETY_ID}/{PRODUCT_ID}.jpg"
            actual=math.ceil(products[3]*0.98)

        
            coin=products[3]*0.02/50
            # print(coin)
            total=total+coin
            products_with_images.append((products[1], products[2], products[3], image_filename,products[0],actual,coin,PRODUCT_ID))
            
        return render_template('cart.html', variety_products=products_with_images,total=total)
    # variety_products.append((xx, products_with_images))
    return render_template('index.html')
@app.route('/pay_now')
def pay_now():

    
    if 'email' in session:
        cur.execute("select address,private_key from FLIP where EMAIL='{}'".format(session['email']))
        record=cur.fetchone()
        private_key=record[1]
        account=record[0]
        # private_key = '24e5ed55a1429f4a38817f1dfe8980450a6667d58c2186ca1d1879128accb7d1'
        ethereum_rpc_url = 'https://polygon-mumbai.blockpi.network/v1/rpc/public'

        # Connect to the Ethereum network
        web3 = Web3(Web3.HTTPProvider(ethereum_rpc_url))

        # Create a wallet instance using the private key
        # account1 = web3.eth.account.privateKeyToAccount(private_key)
        # account='0x03CFAFC676bbfA2CbBA8006c77FBeBEf990031F9'
        token_address = '0x594F38Aa5bd10786B79b09284e844C00cd2917d8'
        token_abi =  [
            {
                "inputs": [],
                "stateMutability": "nonpayable",
                "type": "constructor"
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address"
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address"
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256"
                    }
                ],
                "name": "Approval",
                "type": "event"
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "from",
                        "type": "address"
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "to",
                        "type": "address"
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256"
                    }
                ],
                "name": "Transfer",
                "type": "event"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "owner",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "spender",
                        "type": "address"
                    }
                ],
                "name": "allowance",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "spender",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "amount",
                        "type": "uint256"
                    }
                ],
                "name": "approve",
                "outputs": [
                    {
                        "internalType": "bool",
                        "name": "",
                        "type": "bool"
                    }
                ],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "account",
                        "type": "address"
                    }
                ],
                "name": "balanceOf",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [
                    {
                        "internalType": "uint8",
                        "name": "",
                        "type": "uint8"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "spender",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "subtractedValue",
                        "type": "uint256"
                    }
                ],
                "name": "decreaseAllowance",
                "outputs": [
                    {
                        "internalType": "bool",
                        "name": "",
                        "type": "bool"
                    }
                ],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "spender",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256"
                    }
                ],
                "name": "increaseAllowance",
                "outputs": [
                    {
                        "internalType": "bool",
                        "name": "",
                        "type": "bool"
                    }
                ],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "name",
                "outputs": [
                    {
                        "internalType": "string",
                        "name": "",
                        "type": "string"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "symbol",
                "outputs": [
                    {
                        "internalType": "string",
                        "name": "",
                        "type": "string"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "to",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "amount",
                        "type": "uint256"
                    }
                ],
                "name": "transfer",
                "outputs": [
                    {
                        "internalType": "bool",
                        "name": "",
                        "type": "bool"
                    }
                ],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "from",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "to",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "amount",
                        "type": "uint256"
                    }
                ],
                "name": "transferFrom",
                "outputs": [
                    {
                        "internalType": "bool",
                        "name": "",
                        "type": "bool"
                    }
                ],
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]
        token_contract = web3.eth.contract(address=token_address, abi=token_abi)
        recipient_address = '0x03CFAFC676bbfA2CbBA8006c77FBeBEf990031F9'
        user_id=session['email']
        cur.execute("SELECT PRODUCT_ID from Cart WHERE user_id = :user_id", {"user_id": user_id})
        product_ids = cur.fetchall()
        # products_with_images = []
        total=0
        for product in product_ids:
            PRODUCT_ID=product[0]
            cur.execute("SELECT VARIETY_ID, PRODUCT_NAME, DESCRIPTION, PRICE FROM PRODUCTS WHERE PRODUCT_ID = :PRODUCT_ID", {"PRODUCT_ID": PRODUCT_ID})
            products = cur.fetchone()
            VARIETY_ID = products[0]
            # image_filename = f"static/images/{VARIETY_ID}/{PRODUCT_ID}.jpg"
            actual=math.ceil(products[3]*0.98)

        
            coin=products[3]*0.02/50
            # print(coin)
            total=total+coin
            
            # products_with_images.append((products[1], products[2], products[3], image_filename,products[0],actual,coin,PRODUCT_ID))
        balance = token_contract.functions.balanceOf(account).call()
        balance=balance/pow(10,18)
        if balance<total:
            flash("Not enough balance")
            
            return render_template('error.html',ff=total-balance)

        amount_to_send = web3.to_wei(total, 'ether')  # 10 tokens (adjust decimals as needed)


        transaction = token_contract.functions.transfer(recipient_address, amount_to_send).build_transaction({
            'chainId': 80001,
            'gas': 2000000,
            'gasPrice': web3.to_wei('50', 'gwei'),
            'nonce': web3.eth.get_transaction_count(account),
        })

        signed_txn = web3.eth.account.sign_transaction(transaction,private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print('Transfer successful:', receipt)
        cur.execute("DELETE FROM CART WHERE user_id=:user_id",{"user_id":user_id})
        conn.commit()
        for product in product_ids:
            PRODUCT_ID=product[0]

            sql="INSERT INTO orders(user_id ,PRODUCT_ID  ) VALUES(:user_id,:PRODUCT_ID)"
            cur.execute(sql,[user_id,PRODUCT_ID])
            conn.commit()
            # cur.execute("SELECT VARIETY_ID, PRODUCT_NAME, DESCRIPTION, PRICE FROM PRODUCTS WHERE PRODUCT_ID = :PRODUCT_ID", {"PRODUCT_ID": PRODUCT_ID})
            # products = cur.fetchone()
            # VARIETY_ID = products[0]
            # image_filename = f"static/images/{VARIETY_ID}/{PRODUCT_ID}.jpg"
            # actual=math.ceil(products[3]*0.98)

        
            # coin=math.ceil(products[3]*0.02)
            # print(coin)
            # total=total+coin
        return redirect(url_for('display'))

@app.route('/orders')
def orders():
    # def display():
    if 'email' in session:
        user_id=session['email']
        cur.execute("SELECT PRODUCT_ID from orders WHERE user_id = :user_id", {"user_id": user_id})
        product_ids = cur.fetchall()
        products_with_images = []
        total=0
        for product in product_ids:
            PRODUCT_ID=product[0]
            cur.execute("SELECT VARIETY_ID, PRODUCT_NAME, DESCRIPTION, PRICE FROM PRODUCTS WHERE PRODUCT_ID = :PRODUCT_ID", {"PRODUCT_ID": PRODUCT_ID})
            products = cur.fetchone()
            VARIETY_ID = products[0]
            image_filename = f"static/images/{VARIETY_ID}/{PRODUCT_ID}.jpg"
            actual=math.ceil(products[3]*0.98)

        
            coin=products[3]*0.02/50
            # print(coin)
            total=total+coin
            products_with_images.append((products[1], products[2], products[3], image_filename,products[0],actual,coin,PRODUCT_ID))
            
        return render_template('orders.html', variety_products=products_with_images,total=total)
    # variety_products.append((xx, products_with_images))
    return render_template('index.html')
@app.route('/cart')
def cart():
    if 'email' in session:
        user_id=session['email']
        PRODUCT_ID = request.args.get('variable')
        sql="INSERT INTO Cart(user_id ,PRODUCT_ID  ) VALUES(:user_id,:PRODUCT_ID)"
        cur.execute(sql,[user_id,PRODUCT_ID])
        conn.commit()
        return redirect(url_for('home'))
        

    return render_template('index.html')


@app.route('/logout')
def logout():
    session.pop('email',None)

    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    
    if request.method=='POST':
        username=request.form['user']
        password=request.form['passwd']
        print(username)
        cur.execute("select * from FLIP where EMAIL='{}'".format(username))
        record=cur.fetchone()

        print(record)
        if record:
            # hashed_password=record[1]
            if record[1]==0:
                flash("Email not verified")
                return render_template('index.html')
            elif(hashlib.sha256(password.encode('utf-8')).hexdigest()==record[4]):
            # elif(bcrypt.checkpw(password,record[1])):
                # session.permanent=True
                session['email']=record[0]
                # print("hi")
                return redirect(url_for('home')) #dashboard
            else:
                flash("Incorrect password")
                return render_template('index.html')
                # return redirect(url_for('home')) #dashboard
    # else:
    #     if "username" in session:
    #         return redirect(url_for('user'))
        
    flash("Incorrect username or password") 
    return render_template('index.html')
@app.route("/profile")
def profile():
    if 'email' not in session:
        flash("YOU ARE NOT LOGGED IN")
        return render_template("index.html")
    # cur.execute("select * From SCORES where username='{}'".format(session['username']))
    # abc=cur.fetchone()
    # cur.execute("select * from EDUKIDS where username='{}'".format(session['username']))
    # xx=cur.fetchone()
    # cur.execute("SELECT COUNT(*) FROM SCORES WHERE (LETTER+DIGITS+SHAPES+MISSINGG+MATHS) >= (SELECT (LETTER+DIGITS+SHAPES+MISSINGG+MATHS) FROM SCORES WHERE USERNAME = '{}')".format(session['username']))
    # rank=cur.fetchone()
    # cur.execute("SELECT * FROM TIME_PARENT WHERE USERNAME='{}'".format(session['username']))
    # ff=cur.fetchone()
    cur.execute("SELECT * FROM FLIP WHERE EMAIL='{}'".format(session['email']))
    abc=cur.fetchone()

    return render_template("profile.html",abc=abc)
@app.route("/earncoins")
def earncoins():
    if 'email' not in session:
        flash("YOU ARE NOT LOGGED IN")
        return render_template("index.html")
    # cur.execute("select * From SCORES where username='{}'".format(session['username']))
    # abc=cur.fetchone()
    # cur.execute("select * from EDUKIDS where username='{}'".format(session['username']))
    # xx=cur.fetchone()
    # cur.execute("SELECT COUNT(*) FROM SCORES WHERE (LETTER+DIGITS+SHAPES+MISSINGG+MATHS) >= (SELECT (LETTER+DIGITS+SHAPES+MISSINGG+MATHS) FROM SCORES WHERE USERNAME = '{}')".format(session['username']))
    # rank=cur.fetchone()
    # cur.execute("SELECT * FROM TIME_PARENT WHERE USERNAME='{}'".format(session['username']))
    # ff=cur.fetchone()
    private_key = 'YOUR_PRIVATE_KEY'
    ethereum_rpc_url = 'https://polygon-mumbai.blockpi.network/v1/rpc/public'

    # Connect to the Ethereum network
    web3 = Web3(Web3.HTTPProvider(ethereum_rpc_url))

# Create a wallet instance using the private key
    
    # account = web3.eth.account.privateKeyToAccount(private_key)
    cur.execute("select address from FLIP where EMAIL='{}'".format(session['email']))
    record=cur.fetchone()
    account=record[0]
    # print(account)
    token_address = '0x594F38Aa5bd10786B79b09284e844C00cd2917d8'
    token_abi = [
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Approval",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Transfer",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			}
		],
		"name": "allowance",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "approve",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "account",
				"type": "address"
			}
		],
		"name": "balanceOf",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "decimals",
		"outputs": [
			{
				"internalType": "uint8",
				"name": "",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "subtractedValue",
				"type": "uint256"
			}
		],
		"name": "decreaseAllowance",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "addedValue",
				"type": "uint256"
			}
		],
		"name": "increaseAllowance",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "name",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "symbol",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "totalSupply",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "transfer",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "transferFrom",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]  # Replace with actual ERC20 token ABI
    # print(account)
    token_contract = web3.eth.contract(address=token_address, abi=token_abi)
    balance = token_contract.functions.balanceOf(account).call()
    balance=balance/pow(10,18)
#     transfer_event_signature = web3.keccak(text="Transfer(address,address,uint256)").hex()
    etherscan_api_key = 'J49T31XAKNJCEA37N4AEY1P3ZJ3E2G9NUM'
# account_address = 'YOUR_ACCOUNT_ADDRESS'
# contract_address = 'YOUR_ERC20_TOKEN_ADDRESS'

# Set the Etherscan API URL
    api_url = f'https://api-testnet.polygonscan.com/api?module=account&action=tokentx&address={account}&contractaddress={token_address}&apikey={etherscan_api_key}'

    # Send the API request
    response = requests.get(api_url)
    data = response.json()['result']
    # print(data)
    # Print the token transfer events
    ff=[]

    for tx in data:
        # sender = tx["from"]
        # recipient = tx["to"]
        amount = int(tx["value"]) / 10**18  # Convert from Wei to token units
        timestamp = int(tx['timeStamp'])
        date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        # print(f"Sender: {sender}")
        # print(f"Recipient: {recipient}")
        # print(f"Amount: {amount} Tokens")
        # print("---")   
        ff.append((amount,date))
        
    return render_template("earncoins.html",balance=balance)
@app.route("/activity")
def activity():
    
    if 'email' not in session:
        flash("YOU ARE NOT LOGGED IN")
        return render_template("index.html")
    # cur.execute("select * From SCORES where username='{}'".format(session['username']))
    # abc=cur.fetchone()
    # cur.execute("select * from EDUKIDS where username='{}'".format(session['username']))
    # xx=cur.fetchone()
    # cur.execute("SELECT COUNT(*) FROM SCORES WHERE (LETTER+DIGITS+SHAPES+MISSINGG+MATHS) >= (SELECT (LETTER+DIGITS+SHAPES+MISSINGG+MATHS) FROM SCORES WHERE USERNAME = '{}')".format(session['username']))
    # rank=cur.fetchone()
    # cur.execute("SELECT * FROM TIME_PARENT WHERE USERNAME='{}'".format(session['username']))
    # ff=cur.fetchone()
    private_key = 'YOUR_PRIVATE_KEY'
    ethereum_rpc_url = 'https://polygon-mumbai.blockpi.network/v1/rpc/public'

    # Connect to the Ethereum network
    web3 = Web3(Web3.HTTPProvider(ethereum_rpc_url))

# Create a wallet instance using the private key
    
    # account = web3.eth.account.privateKeyToAccount(private_key)
    cur.execute("select address from FLIP where EMAIL='{}'".format(session['email']))
    record=cur.fetchone()
    account=record[0]
    # print(account)
    token_address = '0x594F38Aa5bd10786B79b09284e844C00cd2917d8'
    token_abi = [
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Approval",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Transfer",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			}
		],
		"name": "allowance",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "approve",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "account",
				"type": "address"
			}
		],
		"name": "balanceOf",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "decimals",
		"outputs": [
			{
				"internalType": "uint8",
				"name": "",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "subtractedValue",
				"type": "uint256"
			}
		],
		"name": "decreaseAllowance",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "addedValue",
				"type": "uint256"
			}
		],
		"name": "increaseAllowance",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "name",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "symbol",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "totalSupply",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "transfer",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "transferFrom",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]  # Replace with actual ERC20 token ABI

    token_contract = web3.eth.contract(address=token_address, abi=token_abi)
    balance = token_contract.functions.balanceOf(account).call()
    balance=balance/pow(10,18)
#     transfer_event_signature = web3.keccak(text="Transfer(address,address,uint256)").hex()
    etherscan_api_key = 'J49T31XAKNJCEA37N4AEY1P3ZJ3E2G9NUM'
# account_address = 'YOUR_ACCOUNT_ADDRESS'
# contract_address = 'YOUR_ERC20_TOKEN_ADDRESS'

# Set the Etherscan API URL
    api_url = f'https://api-testnet.polygonscan.com/api?module=account&action=tokentx&address={account}&contractaddress={token_address}&apikey={etherscan_api_key}'

    # Send the API request
    response = requests.get(api_url)
    data = response.json()['result']
    print(data)
    # Print the token transfer events
    ff=[]

    for tx in data:
        sender = tx["from"]
        recipient = tx["to"]
        amount = int(tx["value"]) / 10**18  # Convert from Wei to token units
        timestamp = int(tx['timeStamp'])
        date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        # print(f"Sender: {sender}")
        # print(f"Recipient: {recipient}")
        # print(f"Amount: {amount} Tokens")
        # print("---")  
        # print(sender.upper())
        # print(account) 
        if(sender.upper()==account.upper()):
            amount="-"+str(amount)
        else:
            amount="+"+str(amount)
        # if(sender.upper()=='0x03CFAFC676bbfA2CbBA8006c77FBeBEf990031F9'.upper()):
        #     sender_name="FlipMart"
        # else:
        #     xx=sender.upper()
        #     cur.execute("select first,second from FLIP where address='{}'".format(xx))
        #     name=cur.fetchone()
        #     sender_name=name[0]+" "+name[1]
        # if(recipient.upper()=='0x03CFAFC676bbfA2CbBA8006c77FBeBEf990031F9'.upper()):
            
        #     receiver_name="FlipMart"
        # else:
        #     print(recipient.upper())
        #     xx=recipient.upper()
        #     cur.execute("select first,second from FLIP where address='{}'".format(xx))
        #     # receiver_name=cur.fetchone()
        #     name=cur.fetchone()
        #     receiver_name=name[0]+" "+name[1]
        ff.append((amount,date))
    
    return render_template("activity.html",ff=ff)

@app.route("/donatecoins",methods=['GET','POST'])
def donatecoins():
    if 'email' not in session:
        flash("YOU ARE NOT LOGGED IN")
        return render_template("index.html")
    # cur.execute("select * From SCORES where username='{}'".format(session['username']))
    # abc=cur.fetchone()
    # cur.execute("select * from EDUKIDS where username='{}'".format(session['username']))
    # xx=cur.fetchone()
    # cur.execute("SELECT COUNT(*) FROM SCORES WHERE (LETTER+DIGITS+SHAPES+MISSINGG+MATHS) >= (SELECT (LETTER+DIGITS+SHAPES+MISSINGG+MATHS) FROM SCORES WHERE USERNAME = '{}')".format(session['username']))
    # rank=cur.fetchone()
    # cur.execute("SELECT * FROM TIME_PARENT WHERE USERNAME='{}'".format(session['username']))
    # ff=cur.fetchone()
    if request.method=='POST':
        
        total=request.form['donationAmount']
        to=request.form['ngoSelect']
        cur.execute("select address,private_key from FLIP where EMAIL='{}'".format(session['email']))
        record=cur.fetchone()
        private_key=record[1]
        account=record[0]
        # cur.execute("select address,private_key from FLIP where FIRST='{}'".format(to))
        # private_key = '24e5ed55a1429f4a38817f1dfe8980450a6667d58c2186ca1d1879128accb7d1'
        ethereum_rpc_url = 'https://polygon-mumbai.blockpi.network/v1/rpc/public'

        # Connect to the Ethereum network
        web3 = Web3(Web3.HTTPProvider(ethereum_rpc_url))

        # Create a wallet instance using the private key
        # account1 = web3.eth.account.privateKeyToAccount(private_key)
        # account='0x03CFAFC676bbfA2CbBA8006c77FBeBEf990031F9'
        token_address = '0x594F38Aa5bd10786B79b09284e844C00cd2917d8'
        token_abi =  [
            {
                "inputs": [],
                "stateMutability": "nonpayable",
                "type": "constructor"
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address"
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "spender",
                        "type": "address"
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256"
                    }
                ],
                "name": "Approval",
                "type": "event"
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "from",
                        "type": "address"
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "to",
                        "type": "address"
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "value",
                        "type": "uint256"
                    }
                ],
                "name": "Transfer",
                "type": "event"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "owner",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "spender",
                        "type": "address"
                    }
                ],
                "name": "allowance",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "spender",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "amount",
                        "type": "uint256"
                    }
                ],
                "name": "approve",
                "outputs": [
                    {
                        "internalType": "bool",
                        "name": "",
                        "type": "bool"
                    }
                ],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "account",
                        "type": "address"
                    }
                ],
                "name": "balanceOf",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [
                    {
                        "internalType": "uint8",
                        "name": "",
                        "type": "uint8"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "spender",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "subtractedValue",
                        "type": "uint256"
                    }
                ],
                "name": "decreaseAllowance",
                "outputs": [
                    {
                        "internalType": "bool",
                        "name": "",
                        "type": "bool"
                    }
                ],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "spender",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "addedValue",
                        "type": "uint256"
                    }
                ],
                "name": "increaseAllowance",
                "outputs": [
                    {
                        "internalType": "bool",
                        "name": "",
                        "type": "bool"
                    }
                ],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "name",
                "outputs": [
                    {
                        "internalType": "string",
                        "name": "",
                        "type": "string"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "symbol",
                "outputs": [
                    {
                        "internalType": "string",
                        "name": "",
                        "type": "string"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "to",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "amount",
                        "type": "uint256"
                    }
                ],
                "name": "transfer",
                "outputs": [
                    {
                        "internalType": "bool",
                        "name": "",
                        "type": "bool"
                    }
                ],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "from",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "to",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "amount",
                        "type": "uint256"
                    }
                ],
                "name": "transferFrom",
                "outputs": [
                    {
                        "internalType": "bool",
                        "name": "",
                        "type": "bool"
                    }
                ],
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]
        token_contract = web3.eth.contract(address=token_address, abi=token_abi)
        recipient_address = '0x881Ea6138c61C8c4a56ba8405DEd31E48362D383'
        user_id=session['email']
        # cur.execute("SELECT PRODUCT_ID from Cart WHERE user_id = :user_id", {"user_id": user_id})
        # product_ids = cur.fetchall()
        # products_with_images = []
        # total=0
        # for product in product_ids:
        #     PRODUCT_ID=product[0]
        #     cur.execute("SELECT VARIETY_ID, PRODUCT_NAME, DESCRIPTION, PRICE FROM PRODUCTS WHERE PRODUCT_ID = :PRODUCT_ID", {"PRODUCT_ID": PRODUCT_ID})
        #     products = cur.fetchone()
        #     VARIETY_ID = products[0]
        #     # image_filename = f"static/images/{VARIETY_ID}/{PRODUCT_ID}.jpg"
        #     actual=math.ceil(products[3]*0.98)

        
        #     coin=products[3]*0.02/50
        #     # print(coin)
        #     total=total+coin
            
            # products_with_images.append((products[1], products[2], products[3], image_filename,products[0],actual,coin,PRODUCT_ID))
        balance = token_contract.functions.balanceOf(account).call()
        balance=balance/pow(10,18)
        if balance<float(total):
            flash("Not enough balance")
            
            return render_template('error.html',ff=total-balance)

        amount_to_send = web3.to_wei(total, 'ether')  # 10 tokens (adjust decimals as needed)


        transaction = token_contract.functions.transfer(recipient_address, amount_to_send).build_transaction({
            'chainId': 80001,
            'gas': 2000000,
            'gasPrice': web3.to_wei('50', 'gwei'),
            'nonce': web3.eth.get_transaction_count(account),
        })

        signed_txn = web3.eth.account.sign_transaction(transaction,private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print('Transfer successful:', receipt)
        receiver_email="sanjoliagarwal123@gmail.com"

        sql="INSERT INTO donate(sender_email ,receiver_email,amount_sent  ) VALUES(:user_id,:receiver_email,:total)"
        cur.execute(sql,[user_id,receiver_email],total)
        conn.commit()
        # cur.execute("DELETE FROM CART WHERE user_id=:user_id",{"user_id":user_id})
        # conn.commit()
        # for product in product_ids:
        #     PRODUCT_ID=product[0]

        #     sql="INSERT INTO orders(user_id ,PRODUCT_ID  ) VALUES(:user_id,:PRODUCT_ID)"
        #     cur.execute(sql,[user_id,PRODUCT_ID])
        #     conn.commit()
            # cur.execute("SELECT VARIETY_ID, PRODUCT_NAME, DESCRIPTION, PRICE FROM PRODUCTS WHERE PRODUCT_ID = :PRODUCT_ID", {"PRODUCT_ID": PRODUCT_ID})
            # products = cur.fetchone()
            # VARIETY_ID = products[0]
            # image_filename = f"static/images/{VARIETY_ID}/{PRODUCT_ID}.jpg"
            # actual=math.ceil(products[3]*0.98)

        
            # coin=math.ceil(products[3]*0.02)
            # print(coin)
            # total=total+coin
        return render_template("thank.html")
    cur.execute("select * from donate where sender_email='{}'".format(session['email']))
    rec= cur.fetchall()


    return render_template("donatecoins.html",rec=rec)
@app.route("/rewards")
def rewards():
    if 'email' not in session:
        flash("YOU ARE NOT LOGGED IN")
        return render_template("index.html")
    # cur.execute("select * From SCORES where username='{}'".format(session['username']))
    # abc=cur.fetchone()
    # cur.execute("select * from EDUKIDS where username='{}'".format(session['username']))
    # xx=cur.fetchone()
    # cur.execute("SELECT COUNT(*) FROM SCORES WHERE (LETTER+DIGITS+SHAPES+MISSINGG+MATHS) >= (SELECT (LETTER+DIGITS+SHAPES+MISSINGG+MATHS) FROM SCORES WHERE USERNAME = '{}')".format(session['username']))
    # rank=cur.fetchone()
    # cur.execute("SELECT * FROM TIME_PARENT WHERE USERNAME='{}'".format(session['username']))
    # ff=cur.fetchone()
    return render_template("rewards.html")
@app.route("/user")
def user():
    # username=session['username']
    if "email" in session:
        # print("hiiiiiiiii")
        return redirect(url_for('home'))
    else:
        return render_template('index.html')  
@app.route('/validate',methods=['GET','POST'])
def validate():
    if request.method=='POST':
        if 'email' in session:
            # print("hi")j
            priv=secrets.token_hex(32)
            private_key="0x"+priv
            account=Account.from_key(private_key)
            acc=account.address
            email=session['email']
            # print(username)
            cur.execute("update FLIP set VERIFYY={} where EMAIL='{}'".format(1,email))
            conn.commit()
            cur.execute("update FLIP set ADDRESS='{}' where EMAIL='{}'".format(acc,email))
            conn.commit()
            cur.execute("update FLIP set PRIVATE_KEY='{}' where EMAIL='{}'".format(private_key,email))
            conn.commit()
            conn.commit()
            session.pop('email',None)
            # return redirect(url_for('user'))
            return render_template('index.html')
        else:
            flash("OTP NOT CORRECT")
            return render_template('verify.html')
    # if request.method=='POST':
@app.route('/final_reset',methods=['GET','POST'])
def final_reset():
    if request.method=='POST':
        if 'reset' in session:
            # print("hi")j
            passwd=encrpt(request.form['pass'])

            mail=session['reset']
            # print(username)
            cur.execute("update EDUKIDS set PASSWORD='{}' where EMAIL='{}'".format(passwd,mail))
            conn.commit()
            session.pop('reset',None)
            return redirect(url_for('hello_world'))
        
    # if request.method=='POST':
@app.route('/validate_new',methods=['GET','POST'])
def validate_new():
    if request.method=='POST':
        return render_template('changepass.html')
    # if request.method=='POST':   
@app.route('/signin',methods=['GET','POST'])
def signin():
    msg=''
    if request.method=='POST':
        First_name=request.form['first']
        Second_name=request.form['second']
        email=request.form['email']
        password=encrpt(request.form['passwd'])
        age=int(request.form['age'])
        gender=request.form['gender']
        phone = request.form['phone']
        # address = request.form['address']
        # salt=bcrypt.gensalt()
        # password=bcrypt.hashpw(passwordd.encode('utf-8'),salt)
        x=0
        # print("hi")
        cur.execute("select * from FLIP where email='{}'".format(email))
        if cur.fetchone():
            flash("Email already used")
            return render_template('signin.html')
        # cur.execute(f"INSERT INTO EDUKIDS VALUES('{username}','{password}',{x},'{First_name}','{Second_name}',{age},'{gender}','{mail}')")
        



        sql="INSERT INTO FLIP(EMAIL ,VERIFYY ,FIRST ,SECOND ,PASSWORD,AGE ,GENDER , PHONE ) VALUES(:email,:x,:First_name,:Second_name,:password,:age,:gender,:phone)"
        cur.execute(sql,[email,x,First_name,Second_name,password,age,gender,phone])
        conn.commit()
        code=verify(email) 
        # cur.execute("select * from EDUKIDS where username='{}' and password='{}'".format(username,password))
        session['email']=email
        return render_template('verify.html',code=code)
    else:
        # flash("Enter Correctly")
        return render_template('signin.html') 

       
 
    #     record=cur.fetchone()
    #     # print(record)
    #     if record:
    #         session['loggedin']=True
    #         session['username']=record[0]
    #         return redirect(url_for('home'))
    #     else:
    #         msgg=message_flashed("Incorrect username or password")
    # return render_template('index.html',msg=msgg)
@app.route('/reset',methods=['GET','POST'])
def reset():
    msg=''
    if request.method=='POST':
        mail=request.form['mail']
        cur.execute("SELECT * FROM EDUKIDS WHERE EMAIL='{}'".format(mail))
        record=cur.fetchone()
        if(record):
            code=reset_pass(mail)
            session['reset']=mail
            return render_template('reset.html',code=code)


        else:
            msg='EMAIL NOT REGISTERED'
            return render_template('forgotpass.html',msg=msg)        
@app.route('/forget_pass')
def forget_pass():
    return render_template('forgotpass.html')
# @app.route('/hand_count')
# def hand_count():

if __name__=="__main__":
    app.run(debug=True)
