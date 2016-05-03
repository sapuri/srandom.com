<?php
function connectDb(){
	try{
		return new PDO(DSN, DB_USER, DB_PASSWORD, array(PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION));
	}catch (PDOException $e){
		echo $e->getMessage();
		exit;
	}
}
