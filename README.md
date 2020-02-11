# boardgame recorder(web)

## What I use
* server
	
	* python, python-library(flask)
	
	  > app.py(Controller) , _2_DB.py(Model)
* view-page
	
	* html,js,css,js-library(chart.js),css-library(bootstrap:sb-admin-2)
	
	  > /templates(html) , /static(js,css)
* db
	
	* sqlite
	
	  > /db
* virtualenv
	
	> /env

## how to make
1. draft 
	
	* [To see draft](https://ovenapp.io/view/0fHwZEjv0dXe8MVQiyUst0SbL7GxPHf7/FCMaf)
2. model db structure(Entity Relationship Modeling)
	* [ERD(Entity Relationship Diagram)](https://drive.google.com/file/d/13pTfod8LuQ-BndJFwpqOv3hU0ESXrTvN/view?usp=sharing)
	* [ERD_db_modeling](https://drive.google.com/file/d/1uEMM3drNv9gBRWHzm8pryigADE10v3sS/view?usp=sharing)
	* db : create table
3. make page
	
	* view-page
4. make functions
	* View < -- > Controller < -- > Model < -- > db
		1. View
			* Responsive web design(반응형 웹 디자인)(bootstrap)
		2. View < -- > Controller
			* rest api (fetch(async,await),json)
		3. Controller
			* flask
		4. Model
			* sqlite3, decorator
		5. db
			* sqlite


## deployed page
on the heroku [page](https://flaskcrudboardgameapp2.herokuapp.com/)