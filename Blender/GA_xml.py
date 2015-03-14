Library = {}

Library["Tree"] = """
<rules max_depth="200">
    <rule name="entry">
        <call  rule="spiral"/>
    </rule>
    <rule name="spiral" weight="100">
        <instance shape="tubey"/>
        <call transforms="tz 0.4 rx 1 sa 0.995" rule="spiral"/>
    </rule>
    <rule name="spiral" weight="100">
        <instance shape="tubey"/>
        <call transforms="tz 0.4 rx 1 ry 1 sa 0.995" rule="spiral"/>
    </rule>
    <rule name="spiral" weight="100">
        <instance shape="tubey"/>
        <call transforms="tz 0.4 rx 1 rz -1 sa 0.995" rule="spiral"/>
    </rule>
    <rule name="spiral" weight="6">
        <call transforms="rx 15" rule="spiral"/>
        <call transforms="rz 180" rule="spiral"/>
    </rule>
</rules>"""

Library["Octopod"] = """
<rules max_depth="20">
    <rule name="entry">
        <call count="300" transforms="rx 3.6" rule="arm"/>
    </rule>
    <rule name="arm">
        <call transforms="sa 0.9 ry 6 tz 1" rule="arm"/>
        <instance transforms="s 0.2 0.5 1" shape="box"/>
    </rule>
    <rule name="arm">
        <call transforms="sa 0.9 ry -6 tz 1" rule="arm"/>
        <instance transforms="s 0.2 0.5 1" shape="sphere"/>
    </rule>
</rules>
"""

Library["Nouveau"] = """
<rules max_depth="2000">
    <rule name="entry">
        <call count="16" transforms="rz 20" rule="hbox"/>
    </rule>
    <rule name="hbox"><call rule="r"/></rule>
    <rule name="r"><call rule="forward"/></rule>
    <rule name="r"><call rule="turn"/></rule>
    <rule name="r"><call rule="turn2"/></rule>
    <rule name="r"><call rule="turn4"/></rule>
    <rule name="r"><call rule="turn3"/></rule>
    <rule name="forward" max_depth="90" successor="r">
        <call rule="dbox"/>
        <call transforms="rz 2 tx 0.1 sa 0.996" rule="forward"/>
    </rule>
    <rule name="turn" max_depth="90" successor="r">
        <call rule="dbox"/>
        <call transforms="rz 2 tx 0.1 sa 0.996" rule="turn"/>
    </rule>
    <rule name="turn2" max_depth="90" successor="r">
        <call rule="dbox"/>
        <call transforms="rz -2 tx 0.1 sa 0.996" rule="turn2"/>
    </rule>
    <rule name="turn3" max_depth="90" successor="r">
        <call rule="dbox"/>
        <call transforms="ry -2 tx 0.1 sa 0.996" rule="turn3"/>
    </rule>
    <rule name="turn4" max_depth="90" successor="r">
        <call rule="dbox"/>
        <call transforms="ry -2 tx 0.1 sa 0.996" rule="turn4"/>
    </rule>
    <rule name="turn5" max_depth="90" successor="r">
        <call rule="dbox"/>
        <call transforms="rx -2 tx 0.1 sa 0.996" rule="turn5"/>
    </rule>
    <rule name="turn6" max_depth="90" successor="r">
        <call rule="dbox"/>
        <call transforms="rx -2 tx 0.1 sa 0.996" rule="turn6"/>
    </rule>
    <rule name="dbox">
        <instance transforms="s 0.55 2.0 1.25 ry 90 rz 45" shape="boxy"/>
    </rule>
</rules>
"""

Library["Spirals"] = """
<rules max_depth="400">
    <rule name="entry">
        <call count="3" transforms="ry 120" rule="R1"/>
        <call count="3" transforms="ry 120" rule="R2"/>
    </rule>
    <rule name="R1" >
        <call transforms="tz 1.3 rz 1.57 ry 6 rx 3 sa 0.99" rule="R1"/>
        <instance transforms="sa 4" shape="sphere"/>
    </rule>
    <rule name="R2">
        <call transforms="tz -1.3 ry 6 rx 3 sa 0.99" rule="R2"/>
        <instance transforms="sa 4" shape="sphere"/>
    </rule>
</rules>
"""

Library["SpiralsBumpy"] = """
<rules max_depth="400">
    <rule name="entry">
        <call count="3" transforms="ry 120" rule="R1"/>
        <call count="3" transforms="ry 120" rule="R2"/>
    </rule>
    <rule name="R1" >
        <call transforms="tz 1.3 rz 1.57 ry 6 rx 3 sa 0.99" rule="R1"/>
        <instance transforms="sa 4" shape="sphere"/>
    </rule>
    <rule name="R2">
        <call transforms="tz -1.3 ry 6 rx 3 sa 0.99" rule="R2"/>
        <instance transforms="sa 4" shape="sphere"/>
    </rule>
    <rule name="R2">
        <call transforms="tz -1.3 ry 6 rx 3 sa 0.99" rule="R2"/>
        <instance transforms="sa 8" shape="sphere"/>
    </rule>
</rules>
"""

Library["ManyBranches"] = """
<rules max_depth="40">
    <rule name="entry">
        <call rule="R1"/>
    </rule>
    <rule name="R1" weight = "10">
        <call transforms="tz 0.6 rx 5 ry 5 sa 0.99" rule="R1"/>
        <instance shape="box"/>
    </rule>
    <rule name="R1" weight="1">
        <call transforms="rx 10 rz 20" rule="R1"/>
        <call transforms="ry 20" rule="R1"/>
    </rule>
</rules>
"""

Library["ArcSphere"] = """
<rules max_depth="40">
    <rule name="entry">
        <call count="7" transforms="s 0.9 tx -2 ty 0.5" rule="R1"/>
    </rule>
    
    <rule name="R1" weight = "40">
        <call rule="ubox"/>
        <call rule="dbox"/>
        <call transforms="tx 1 ry 3" rule="R1"/>
    </rule>
    
    <rule name="R1" weight = "14">
        <call rule="R2"/>
    </rule>
    
    <rule name="R2" weight="10">
        <call transforms="tx 1 ry 3" rule="R2"/>
    </rule>
    
    <rule name="R2" weight="1">
        <call rule="R1"/>
    </rule>
    
    <rule name="dbox" weight="8" maxdepth="15">
        <call transforms="ty -1 rx 2.9" rule="dbox"/>
        <call rule="sbox"/>
    </rule> 
    
    <rule name="dbox">
    </rule> 
    
    <rule name="ubox" weight="8" maxdepth="15">
        <call transforms="ty 1 rx -2.9" rule="ubox"/>
        <call rule="sbox"/>
    </rule> 
        
    <rule name="ubox">
    </rule>   
  
    <rule name="sbox">
        <instance transforms="s 1.2 1.2 0.6 ry 5" shape="box"/> 
    </rule>   
    

</rules>
"""


Library["Default"] = Library["Tree"]