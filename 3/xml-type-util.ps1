
function IterateType([System.Xml.XmlElement]$type, [int]$unwrapCount = 0) {
    [System.Collections.Generic.List[object]]$q = New-Object 'System.Collections.Generic.List[object]'
    [System.Collections.Generic.HashSet[object]]$elementSet = New-Object 'System.Collections.Generic.HashSet[object]'
    $labeledNodes = @{}
    $unwrapCounts = @{}

    $q.Add($type)

    function addChildNodes($childNodes) {
        if ($childNodes.Count -eq 0) {
            return
        } elseif ($childNodes.Count -eq 1) {
            $q.Add($childNodes[0])
        } else {
            $q.AddRange(($childNodes | ForEach-Object { $_ }))
        }
    }

    while ($q.Count -gt 0) {
        $t = $q[0]
        $q.RemoveAt(0)
        if ($null -ne $t.id) {
            $labeledNodes[$t.id] = $t
            $unwrapCounts[$t.id] = 0
        }
        $state = if ($elementSet.Add($t)) {
            'new'
        } else {
            'old'
        }
        switch ($t.Name) {
            'type-ref' {
                if ($unwrapCounts[$t.ref] -lt $unwrapCount) {
                    $unwrapCounts[$t.ref] += 1
                    # $labeledNodes[$t.ref]
                    @{ Node = $labeledNodes[$t.ref]; State = $state }
                    addChildNodes($labeledNodes[$t.ref].ChildNodes)
                }
            }
            Default {
                @{ Node = $t; State = $state }
                addChildNodes($t.ChildNodes)
            }
        }
    }
}

function TypeMetric([System.Xml.XmlElement]$t, [System.Xml.XmlElement]$u, [int]$unwrapCount = 5, [int]$maxIter = 1000) {
    $tUnwrapped = IterateType $t $unwrapCount
    $uUnwrapped = IterateType $u $unwrapCount
    $i = 0

    # TODO: check for unvisited nodes with another set thing.

    while ($i -lt $maxIter) {
        $ti = $tUnwrapped[$i]
        $tu = $uUnwrapped[$i]
        if ($null -eq $ti -and $null -eq $tu) {
            return 0
        } elseif ($null -eq $ti -or $null -eq $tu) {
            return [math]::Pow(2, ($i + 1))
        } elseif ($ti.Node.Name -ne $tu.Node.Name) {
            return [math]::Pow(2, ($i + 1))
        }
        $i += 1
    }
}