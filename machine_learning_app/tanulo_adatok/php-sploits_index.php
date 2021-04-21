<?php
require_once 'common.php';
require_once 'dbfuncs.php';

$getUser = $_REQUEST["username"];
$getId    = $_REQUEST["id"];

// ' UNION SELECT 1,1,1,1,LOAD_FILE('/etc/passwd'),'1

if(!empty($getUser)) {
	$query   = "select * from users where username = '" . $getUser . "'";
	$results = getSelect($query);
}
elseif(!empty($getId)) {
	$query   = "select * from users where id = " . $getId;
	$results = getSelect($query);
}

