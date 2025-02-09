.open "main.dol"
.org 0x80064b54 ; called every frame
bl give_archipelago_item

.close

.open "d_a_b_lastbossNP.rel"
.org 0x9B18 ; hard-code the actor to set story flag 959 when killed
bl set_demise_defeated_storyflag

.close
