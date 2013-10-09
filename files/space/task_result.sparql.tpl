prefix : <http://example.org/lamp/>
prefix sweet:  <http://sweet.jpl.nasa.gov/>
prefix frap: <http://purl.org/frap/>
prefix dul:  <http://www.loa.istc.cnr.it/ontologies/DUL.owl#>
prefix ssn:  <http://www.w3.org/2005/Incubator/ssn/ssnx/ssn#>
prefix ucum:  <http://purl.oclc.org/NET/muo/ucum/>
prefix actuators:  <http://example.org/lamp/actuators/>


select ?ov where {
  actuators:light ssn:madeObservation ?light .
  
  ?light ssn:observedProperty  sweet:Light ;
         ssn:observationResult ?so .
  
  ?so ssn:hasValue ?ov .
  
  ?ov a ssn:ObservationValue ;
      dul:isClassifiedBy  ucum:lux ;
      dul:hasDataValue {{value}} .
}