import Data.List (sort, nub, notElem, elemIndices)

main = do
    input <- getContents
    let es = edges (lines input)
        in case kahn (sources' es) es of
        Left e -> putStrLn e
        Right tasks -> putStr (unlines tasks)

edges [] = []
edges [_] = [] -- this case should never occur  
edges (u:v:ls) = (v, u) : edges ls

keys [] = []
keys ((k, _):ps) = k : keys ps

values [] = []
values ((_, v):ps) = v : values ps

uniq x xs = length (elemIndices x xs) == 1

succs u es = values $ filter (\(v, _) -> u == v) es

sources es = filter (\u -> notElem u (values es)) (keys es)
sources' es = sort (nub (sources es))

leaves es = filter (\v -> notElem v (keys es) && uniq v (values es)) (values es)
leaves' es = sort (nub (leaves es))

leavesOf u es = filter (\v -> elem v (succs u es)) (leaves' es)

prune u es = filter (\(v, w) -> u /= v) es

pruneAll [u] es = prune u es
pruneAll (u:us) es = pruneAll us (prune u es)

kahn [] [] = Right []
kahn [] _ = Left "cycle"
kahn (s:_) es =
    let rs = s : leavesOf s es
        in fmap (rs ++) (kahn (sources' (pruneAll rs es)) (pruneAll rs es))
