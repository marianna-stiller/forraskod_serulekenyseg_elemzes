<?php
if ( isset( $_GET['first_name'], $_GET['last_name'], $_GET['birth_date'] ) ) {

	$update_query = "UPDATE students SET first_name='{$_GET['first_name']}', last_name='{$_GET['last_name']}', birth_date='{$_GET['birth_date']}' WHERE id={$_GET['id']}";

	$result = $pdo->exec( $update_query );

	if ( $result ) {
		?>
		<div class="alert alert-success" role="alert">
			User updated
		</div>
		<?php
	} else {
		?>
		<div class="alert alert-warning" role="alert">
			There was a problem while updating the new user: <?= json_encode( $pdo->errorInfo() ) ?>
		</div>
		<?php
	}
	?>
	<a class="btn btn-primary active" href="?action=search">Back</a>
	<?php
} 
