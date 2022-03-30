<?php


	$sql = new mysqli("cse.unl.edu", "apages", "Wtpt4R", "apages");

	$qry = "SELECT Major.title AS major, uri, subjectId AS subject FROM MajorSubject JOIN Major ON MajorSubject.major_fk = Major.major_key JOIN Subject ON MajorSubject.subject_fk = Subject.subject_key WHERE minorOnly IS FALSE";
	$qry = $sql->prepare($qry);

	$qry->execute();
	$result = $qry->get_result();

	$majors = array();

	while ($row = mysqli_fetch_assoc($result)) {

		$major = $row['major'];
		$subject = $row['subject'];

		if (!array_key_exists($major, $majors)) {
			$majors[$major] = array(
				'uri' => $row['uri'],
				'subjects' => array()
			);
		}

		$majors[$major]['subjects'][] = $subject;
	}

    ksort($majors);
	mysqli_close($sql);
	echo json_encode($majors);

?>
