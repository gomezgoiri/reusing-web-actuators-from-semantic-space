@prefix frap:  <http://purl.org/frap/> .
@prefix dul:  <http://www.loa.istc.cnr.it/ontologies/DUL.owl#> .
@prefix ssn:  <http://www.w3.org/2005/Incubator/ssn/ssnx/ssn#> .
@prefix ucum:  <http://purl.oclc.org/NET/muo/ucum/> .
@prefix : <http://example.org/lamp/>.


# Description of the preference
:obsv a ssn:ObservationValue, frap:Preference ;
      dul:isClassifiedBy  ucum:lux ;
      dul:hasDataValue {{value}} .