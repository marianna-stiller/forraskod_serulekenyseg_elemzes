<?php
$dbh = new PDO('mysql:dbname=testdb;host=127.0.0.1', $user, $password);
$stmt = $dbh->prepare('UPDATE people SET name = :new_name WHERE id = :id');
$stmt->execute( ['new_name' => $name, 'id' => $id] );
