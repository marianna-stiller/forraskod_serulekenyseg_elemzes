<?php
if ( isset( $_GET['first_name'], $_GET['last_name'], $_GET['birth_date'] ) ) {

	$insert_query = 'INSERT INTO students(first_name, last_name, birth_date) VALUES (' .
	                "'{$_GET['first_name']}', '{$_GET['last_name']}', '{$_GET['birth_date']}')";

	$result = $pdo->exec( $insert_query );

	if ( $result ) {
		?>
		<div class="alert alert-success" role="alert">
			User inserted
		</div>
		<?php
	} else {
		?>
		<div class="alert alert-warning" role="alert">
			There was a problem while inserting the new user: <?= json_encode( $pdo->errorInfo() ) ?>
		</div>
		<?php
	}
	?>
	<a class="btn btn-primary active" href="?action=search">Back</a>
	<?php
}
