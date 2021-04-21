<?php
if ( isset( $_GET['first_name'], $_GET['last_name'], $_GET['birth_date'] ) ) {

	$update_query = "UPDATE students SET first_name=:first_name, last_name=:last_name, birth_date=:birth_date WHERE id=:id";

	$prepared_statement = $pdo->prepare( $update_query );
	$prepared_statement->bindParam( 'first_name', $_GET['first_name'] );
	$prepared_statement->bindParam( 'last_name', $_GET['last_name'] );
	$prepared_statement->bindParam( 'birth_date', $_GET['birth_date'] );
	$prepared_statement->bindParam( 'id', $_GET['id'] );
	$prepared_statement->execute();

	$result = $prepared_statement->rowCount();

	if ( $result ) {
		?>
		<div class="alert alert-success" role="alert">
			User updated
		</div>
		<?php
	} else {
		?>
		<div class="alert alert-warning" role="alert">
			There was a problem while updating the user.
		</div>
		<?php
	}
	?>
	<a class="btn btn-primary active" href="?action=search">Back</a>
	<?php
}
