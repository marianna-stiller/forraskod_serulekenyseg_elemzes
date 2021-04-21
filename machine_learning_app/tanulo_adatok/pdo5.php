<?php
$mysqli->query('SET NAMES gbk');
$stmt = $mysqli->prepare('SELECT * FROM test WHERE name = ? LIMIT 1');
$param = "\xbf\x27 OR 1=1 /*";
$stmt->bind_param('s', $param);
$stmt->execute();
