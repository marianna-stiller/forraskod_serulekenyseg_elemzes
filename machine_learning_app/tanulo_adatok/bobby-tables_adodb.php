<?php
$dbConnection = NewADOConnection($connectionString);
$sqlResult = $dbConnection->Execute(
    'SELECT user_id,first_name,last_name FROM users WHERE username=? AND password=?',
    [$_REQUEST['username'], sha1($_REQUEST['password'])]
);
