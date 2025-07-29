#!/usr/bin/env julia

using Distributed;


CFfile = "";
nets = [];
outfile = "qlls.csv";
ncores = 1;

ftolRel = 1e-6
ftolAbs = 1e-6
xtolAbs = 1e-3
xtolRel = 1e-2
up_to_constant = true

# ftolRel = 1e-1
# ftolAbs = 1e-1
# xtolAbs = 1e-1
# xtolRel = 1e-1
seed = 12038

function help_func()
    # make a help message
    help_message = """

    Calculate expected CF and overall pseudolikelihood score from
    a set of defined phylogenetic networks

    Usage: $(PROGRAM_FILE) CFfile [network files]
            --outfile outfile
            --ncores ncores

    Required arguments:
        CFfile: str; file with the CFs
        [network files]: [str]; a set of phylogenetic network files

    Optional arguments:
        --outfile outfile: str; output file name. (default: $outfile)
        --ftolRel: float; relative tolerance for the objective function (default: $ftolRel)
        --ftolAbs: float; absolute tolerance for the objective function (default: $ftolAbs)
        --xtolRel: float; relative tolerance for parameter changes (default: $xtolRel)
        --xtolAbs: float; absolute tolerance for parameter changes  (default: $xtolAbs)
        --no_up_to_constant: do not use the up to constant option. Not up to constant
                   use raw qll pseudolikelihood to estimate overall pseudolikelihood
        --ncores: int; number of cores (default: $ncores)        
        --seed: int; seed for random number generator (default: $seed)
        --help: display this help message
""";
    println(help_message);
    exit(0);    
end

if length(ARGS) < 2
    help_func();
end

# touched another argument?
toa = false

for i in eachindex(ARGS)

    if i == 1 && !startswith( ARGS[i], "--" )
        global CFfile = ARGS[i];
        continue
    end
        
    if !startswith( ARGS[i], "--" ) && !toa
        push!(nets, ARGS[i]);

    else
        global toa = true

        if ARGS[i] == "--ncores"
        global ncores = parse(Int, ARGS[i+1]);

        elseif ARGS[i] == "--outfile"
            global outfile = ARGS[i+1];

        elseif ARGS[i] == "--no_up_to_constant"
            global up_to_constant = false;

        elseif ARGS[i] == "--ftolRel"
            global ftolRel = parse(Float64, ARGS[i+1]);
        
        elseif ARGS[i] == "--ftolAbs"
            global ftolAbs = parse(Float64, ARGS[i+1]);
        
        elseif ARGS[i] == "--xtolRel"
            global xtolRel = parse(Float64, ARGS[i+1]);
        
        elseif ARGS[i] == "--xtolAbs"
            global xtolAbs = parse(Float64, ARGS[i+1]);

        elseif ARGS[i] == "--seed"
            global seed = parse(Int, ARGS[i+1]);

        elseif ARGS[i] == "--help" || ARGS[i] == "-h"
            help_func();
        end
    end

end

if CFfile == "" || length(nets) == 0 
    help_func();
end

# println("CFfile: ", CFfile);
# println("nets : ", length(nets));
# println("outfile: ", outfile);
# println("ncores: ", ncores);

using Suppressor;
using DelimitedFiles

addprocs(ncores)

@everywhere using Random;
@everywhere using CSV;
@suppress @everywhere using DataFrames;
@everywhere using PhyloNetworks;

function get_uniq_names(all_buckyCF)
    # get all the species names
    spps_names = Set{String}()
    for q in all_buckyCF.quartet
        for taxon in q.taxon
            push!(spps_names, taxon)
        end
    end
    # convert spps_names to a vector
    spps_names = collect(spps_names)
    return spps_names
end

@everywhere function  set_spps_names(netstart, spps_names)
    for (i,l) in enumerate(netstart.leaf)
        l.name = spps_names[i]
    end
end

function  make_colnames(dat)
    ordered_spps = []
    for row in eachrow(dat) # O(T^4)
        quartet = Array(row[1:4])
        joined = join(quartet, "'.'")
        push!(ordered_spps, "'" * joined * "'")
    end
    push!(ordered_spps, "sum")

    return ordered_spps
end

@everywhere function q_pseudo(qt; up_to_constant = true)
    if up_to_constant
        return qt.logPseudoLik
    end

    counts = qt.obsCF*qt.ngenes
    # add to the results table
    return sum(counts .* log.(qt.qnet.expCF))
end


function evaluate_sims(networks, buckyCFfile, outputfile, up_to_constant,
    ftolRel, ftolAbs, xtolRel, xtolAbs; seed = 12038)
    
    Random.seed!(seed)
    # buckyCFfile = "./test_data/1_seqgen.CFs.csv"
    # netfile = "./test_data/n6/n6_sim1.txt"

    @everywhere function process_network(netfile, all_buckyCF, permuted_names, up_to_constant,
        ftolRel, ftolAbs, xtolRel, xtolAbs)
        # O(1)

        netstart = readTopology(netfile) # O(n)
        set_spps_names(netstart, permuted_names)

        try
            # branch lengths from simulation are clock time-based
            # and the time snaq considers branch lengths on
            # coalescent units. For that reason we use 
            # topologyMaxQPseudolik!

            # it returns a new network with updated branch lengths
            # and gamma values, which is not stored in any variable here.
            # The original network is not modified.
            # However, what is modified is all_buckyCF
            topologyMaxQPseudolik!(netstart, all_buckyCF, 
                                    ftolRel = ftolRel, 
                                    ftolAbs = ftolAbs, 
                                    xtolRel = xtolRel, 
                                    xtolAbs = xtolAbs)
            # println(new_net)
            qlls = Dict{Tuple,Float64}()
            for qt in all_buckyCF.quartet
                qlls[Tuple(qt.taxon)] = q_pseudo(qt; up_to_constant = up_to_constant)
            end
            # println(qlls)
            return qlls

        catch e
            println("Error in ", netfile, ": ", e)
            return nothing
        end
    end

    all_buckyCF = readTableCF(buckyCFfile)
    # get all the species names
    permuted_names = get_uniq_names(all_buckyCF) # unordered   
    dat = DataFrame(CSV.File(buckyCFfile); copycols=false)

    results = @distributed (vcat) for netfile in networks
        println(netfile)

        all_buckyCF_tmp = deepcopy(all_buckyCF)
        permuted_names = permuted_names[randperm(length(permuted_names))]
        # println("permuted names: ", permuted_names)

        process_network(netfile, all_buckyCF_tmp, permuted_names, up_to_constant,
         ftolRel, ftolAbs, xtolRel, xtolAbs)
    end

    Xy = []
    # add column names, including the `sum`
    push!(Xy, make_colnames(dat))

    # O(n*T^4)
    for qlls_dict in results

        if qlls_dict === nothing
            continue
        end

        # creates a vector with the same order as the data CF table
        xy_i = []
        for row in eachrow(dat) # O(T^4)
            # get the quartet from dat
            quartet = string.(Tuple(row[1:4])) 

            # call from dictionary
            push!(xy_i, qlls_dict[quartet])
        end
        push!(xy_i, sum(xy_i))

        push!(Xy, xy_i)
    end

    writedlm(outputfile, Xy, ',')
end

@time evaluate_sims(nets, CFfile, outfile, up_to_constant, 
ftolRel, ftolAbs, xtolRel, xtolAbs; seed = seed)
