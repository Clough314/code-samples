<?php

	$sql = new mysqli("localhost", "apages", "Wtpt4R", "apages");
	
	$qry = "SELECT Major.title AS minor, uri, subjectId AS subject FROM MajorSubject JOIN Major ON MajorSubject.major_fk = Major.major_key JOIN Subject ON MajorSubject.subject_fk = Subject.subject_key WHERE minorOnly IS TRUE OR minorOffered IS TRUE";
	$qry = $sql->prepare($qry);

	$qry-> execute();
	$result = $qry->get_result();

	$minors = array();

	while ($row = mysqli_fetch_assoc($result)) {

                $minor = $row['minor'];
                $subject = $row['subject'];

                if (!array_key_exists($minor, $minors)) {
                        $minors[$minor] = array(
                                'uri' => $row['uri'],
                                'subjects' => array()
                        );
                }

                $minors[$minor]['subjects'][] = $subject;
        }

    ksort($minors);
    mysqli_close($sql);
	echo json_encode($minors);

?>
