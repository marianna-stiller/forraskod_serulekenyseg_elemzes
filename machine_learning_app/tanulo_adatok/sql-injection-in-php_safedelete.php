<?php
$id = $_GET['id'];

$delete_query = 'DELETE FROM students where id = :id';

$prepared_statement = $pdo->prepare( $delete_query );
$prepared_statement->bindParam( 'id', $id );
$prepared_statement->execute();

$result = $prepared_statement->rowCount();
