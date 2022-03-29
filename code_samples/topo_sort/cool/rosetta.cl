class List {

    isNil(): Bool { true };
    
    head(): Object {{ abort(); ""; }};
    
    tail(): List {{ abort(); self; }};
    
    cons(s: Object) : List {
        (new Cons).init(s, self)
    };

    rev(): List { self };
};

Class Cons inherits List {

    head: Object;
    tail: List;

    isNil(): Bool { false };

    head(): Object { head };

    tail(): List { tail };

    init(s: Object, ss: List): List {{
        head <- s;
        tail <- ss;
        self;
    }};
};

class Edge {

    orig: String;
    dest: String;

    orig(): String { orig };

    dest(): String { dest };

    init(s: String, t: String): Edge {{
        orig <- s;
        dest <- t;
        self;
    }};
};

class Main inherits IO {

    cycle: Bool <- false;

    input(): List {
        let s: String <- in_string(), lines: List <- new List in {
        while not s = "" loop {
            lines <- lines.cons(s);
            s <- in_string();
        } pool;
        lines;
    }};

    edges(l: List): List {
        let es: List <- new List in {
        while not l.isNil() loop {
            let orig: String <- case l.head() of
                s: String => s;
            esac, dest: String <- case l.tail().head() of
                s: String => s;
            esac in
            es <- es.cons((new Edge).init(orig, dest));
            l <- l.tail().tail();
        } pool;
        es;
    }};

    sources(es: List): List {
        let ss: List <- new List, sst: List <- new List, esi: List <- es in {
        while not esi.isNil() loop {
            let u: String <- case esi.head() of
                e: Edge => e.orig();
            esac, esj: List <- es, uniq: Bool <- true in {
            while not esj.isNil() loop {
                let v: String <- case esj.head() of
                    e: Edge => e.dest();
                esac in
                if u = v then
                    uniq <- false
                else
                    0
                fi;
                esj <- esj.tail();
            } pool;
            while not sst.isNil() loop {
                let v: String <- case sst.head() of
                    s: String => s;
                esac in
                if u = v then
                    uniq <- false
                else
                    0
                fi;
                sst <- sst.tail();
            } pool;
            if uniq then
                ss <- ss.cons(u)
            else
                0
            fi;
            sst <- ss;
            };
            esi <- esi.tail();
        } pool;
        ss;
    }};

    remove(x: String, l: List): List {
        let lt: List <- new List, h: String <- case l.head() of
            h: String => h;
        esac in {
        if x = h then
            lt <- l.tail()
        else
            lt <- remove(x, l.tail()).cons(h)
        fi;
        lt;
    }};

    sinks(es: List): List {
        let ss: List <- new List, sst: List <- new List, esi: List <- es in {
        while not esi.isNil() loop {
            let u: String <- case esi.head() of
                e: Edge => e.dest();
            esac, esj: List <- es, uniq: Bool <- true in {
            while not esj.isNil() loop {
                let v: String <- case esj.head() of
                    e: Edge => e.orig();
                esac in
                if u = v then
                    uniq <- false
                else
                    0
                fi;
                esj <- esj.tail();
            } pool;
            while not sst.isNil() loop {
                let v: String <- case sst.head() of
                    s: String => s;
                esac in
                if u = v then
                    uniq <- false
                else
                    0
                fi;
                sst <- sst.tail();
            } pool;
            if uniq then
                ss <- ss.cons(u)
            else
                0
            fi;
            sst <- ss;
            };
            esi <- esi.tail();
        } pool;
        ss;
    }};

    dummify(es: List): List {
        let ss: List <- sinks(es) in {
        while not ss.isNil() loop {
            let h: String <- case ss.head() of
                h: String => h;
            esac in
            es <- es.cons((new Edge).init(h, "~"));
            ss <- ss.tail();
        } pool;
        es;
    }};

    sort(ss: List): List {
        if ss.isNil() then new List else {
        let ssi: List <- ss, sst: List <- new List, max: String <- "" in {
        if ss.tail().isNil() then {
            sst <- (new List).cons(ss.head());
        } else {
            while not ssi.isNil() loop {
                let h: String <- case ssi.head() of
                    h: String => h;
                esac in
                if max < h then
                    max <- h
                else
                    0
                fi;
                ssi <- ssi.tail();
            } pool;
            sst <- sort(remove(max, ss)).cons(max);
        } fi;
        sst;
    }; } fi };

    prune(s: String, es: List): List {
        if not es.isNil() then
            let e: Edge <- case es.head() of
                h: Edge => h;
            esac in
            if s = e.orig() then
                prune(s, es.tail())
            else
                prune(s, es.tail()).cons(e)
            fi
        else
            new List
        fi
    };

    reverse(l: List): List {
        let lt: List <- new List in {
        while not l.isNil() loop {
            lt <- lt.cons(l.head());
            l <- l.tail();
        } pool;
        lt;
    }};

    kahn(ss: List, es: List): List {
        if ss.isNil() then
            if es.isNil() then
                new List
            else
                { cycle <- true; new List; }
            fi
        else {
            let s: String <- case ss.head() of
                s: String => s;
            esac, est: List <- prune(s, es) in {
            kahn(reverse(sort(sources(est))), est).cons(s); };
        } fi
    };

    print(l: List): Object {
        if l.isNil() then
            0
        else {
            case l.head() of
                s: String => {
                    out_string(s);
                    out_string("\n");
                };
                e: Edge => {
                    out_string("(");
                    out_string(e.orig());
                    out_string(", ");
                    out_string(e.dest());
                    out_string(")\n");
                };
            esac;
            print(l.tail());
        } fi
    };

    main(): Object {
        let es: List <- dummify(edges(input())) in {
            let result: List <- kahn(reverse(sort(sources(es))), es) in
            if cycle then out_string("cycle\n") else print(result) fi;
    }};
};
