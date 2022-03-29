let input =
    let lines = ref [] in
    try
        while true; do
            lines := input_line stdin :: !lines
        done; !lines
    with End_of_file ->
        List.rev !lines

let rec edges ls =
    match ls with
    | [] -> []
    | _ :: [] -> [] (* This case never occurs, according to the input specifications *)
    | u :: v :: ls -> (v, u) :: edges ls

(* The `kahn` function doesn't catch leaves, so this extends them with some dummy leaves. *)
(* As long as the input is ASCII, this won't backfire. *)
let rec dummify es = es @ List.map (fun (_, u) -> (u, "☹")) (List.filter (fun (_, u) -> List.for_all (fun (v, _) -> u <> v) es) es)

let sources es = List.map fst (List.filter (fun (u, _) -> List.for_all (fun (_, v) -> u <> v) es) es)

let prune u es = List.filter (fun (v, _) -> u <> v) es

(* Based on pseudocode of Kahn's topological sort. *)
(* This implementation is original afaik. *)
(* Source: https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm. *)
let rec kahn ss es = match ss with
    | [] ->
        if List.length es > 0 then
            raise (Failure "cycle\r")
        else
            []
    | s :: _ ->
        let es_new = prune s es in
        s :: kahn (List.sort_uniq compare (sources es_new)) es_new 

let () =
    try
        let es = dummify (edges input) in
        List.iter print_endline (kahn (List.sort_uniq compare (sources es)) es) 
    with
        Failure message -> print_endline message
