<?php
$stmt = $db->prepare('update people set name = ? where id = ?');
$stmt->bind_param('si',$name,$id);
$stmt->execute();
