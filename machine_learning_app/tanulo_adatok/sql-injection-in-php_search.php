<?php
	$first_name = $_GET['first_name'] ?? '';
	$last_name  = $_GET['last_name'] ?? '';

	$count_query = 'SELECT COUNT(*) as num_rows from students where hidden=0 ';

	$query = 'SELECT id, first_name, last_name, birth_date from students where hidden=0 ';

	$filters = '';

	if (  ! empty( $first_name ) || ! empty( $last_name ) ) {

		if ( isset( $_GET['first_name'] ) && ! empty( $_GET['first_name'] ) ) {
			$filters .= "AND first_name LIKE '%{$_GET['first_name']}%' ";
		}

		if ( isset( $_GET['last_name'] ) && ! empty( $_GET['last_name'] ) ) {
			$filters .= "AND last_name LIKE '%{$_GET['last_name']}%' ";
		}
	}

	$page  = $_GET['page'] ?? 1;
	$query .= $filters . ' LIMIT 5 OFFSET ' . ( $page - 1 ) * 5;

	$result = $pdo->query( $query );

	$count_query = $pdo->query( $count_query . $filters );
	$count_result = $count_query ? $count_query->fetch()['num_rows'] : 0;
	$num_pages = ( $count_result / 5 ) + ( ( $count_result % 5 ) ? 1 : 0 );


?>