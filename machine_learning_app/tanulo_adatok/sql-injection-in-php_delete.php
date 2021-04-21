<?php
$id = $_GET['id'];

$delete_query = 'DELETE FROM students where id = ' . $id;

$result = $pdo->exec( $delete_query );
