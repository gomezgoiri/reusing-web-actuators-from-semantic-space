@prefix frap: <http://purl.org/frap/> .
@prefix http: <http://www.w3.org/2011/http#> .
@prefix sweet:  <http://sweet.jpl.nasa.gov/> .
@prefix dbpedia:  <http://dbpedia.org/resource/> .
@prefix ucum: <http://purl.oclc.org/NET/muo/ucum/> .
@prefix dul: <http://www.loa.istc.cnr.it/ontologies/DUL.owl#>.
@prefix ssn:  <http://www.w3.org/2005/Incubator/ssn/ssnx/ssn#> .


# Heaters with heater actuator
# sth/actuators/heater
{% for heater_name in heater_names %}
@prefix {{ heater_name }}: <http://{{ heater_name }}.net/hvac>.
@prefix {{ heater_name }}act:  <http://{{ heater_name }}.net/hvac/actuators/> .
@prefix {{ heater_name }}meas: <http://{{ heater_name }}.net/hvac/actuators/heater/>. # TODO also redirect to the last one
{% endfor %}


{% for heater_name in heater_names %}
{# sth/hvac/ -> GET #}
{{ heater_name }}:hvac a dbpedia:HVAC ;
      ssn:attachedSystem {{ heater_name }}act:heater .
      
{# sth/hvac/actuators/heater -> GET #}
{{ heater_name }}act:heater a ssn:Sensor;
  ssn:observes sweet:Temperature ; # In quanTemperature.owl
  ssn:onPlatform {{ heater_name }}:hvac .
  {# simplification: just one "measure" #}
  {{ heater_name }}act:heater ssn:madeObservation {{ heater_name }}meas:0 .

{# sth/hvac/actuators/heater -> POST #}
{
  ?obsv a ssn:ObservationValue ;
      a frap:Preference ;
      dul:isClassifiedBy  ucum:kelvin ;
      dul:hasDataValue ?desired_value .
}
=>
{
  _:request http:methodName "POST";
            http:requestURI {{ heater_name }}act:heater ;
            http:body ?desired_value ;
            http:resp [ http:body ?heaterObs ].
  
  {{ heater_name }}act:heater ssn:madeObservation ?heaterObs .
  
  ?heaterObs a ssn:Observation ;
         ssn:observedProperty sweet:Temperature ;
         ssn:observedBy {{ heater_name }}act:heater ;
         ssn:observationResult ?so .
     
  ?so ssn:hasValue ?ov .

  ?ov a ssn:ObservationValue ;
      dul:isClassifiedBy ucum:kelvin ;
      dul:hasDataValue ?desired_value .
}.

{# sth/hvac/actuators/heater/measureX -> GET #}
{
  {{ heater_name }}act:heater ssn:madeObservation ?heater_obs .
}
=>
{
  _:request http:methodName "GET" ;
            http:requestURI ?heaterObs ;
            http:resp [ http:body ?heaterObs ].
  
  ?heaterObs a  ssn:Observation ;
         ssn:observedProperty  sweet:Temperature ;
         ssn:observedBy {{ heater_name }}act:heater ;
         ssn:observationResult ?so .
  
  ?so ssn:hasValue ?ov .
  
  ?ov a ssn:ObservationValue ;
      dul:isClassifiedBy  ucum:kelvin ;
      dul:hasDataValue _:val .
}.

# sth/hvac/actuators/heater/measureX -> GET
{{ heater_name }}meas:0 a ssn:Observation ;
				ssn:observedProperty  sweet:Light ;
				ssn:observedBy {{ heater_name }}act:light ; # redundant madeObservation
				ssn:observationResult {{ heater_name }}meas:or .

{{ heater_name }}meas:or ssn:hasValue {{ heater_name }}meas:ov .

{{ heater_name }}meas:ov a ssn:ObservationValue ;
    	   dul:isClassifiedBy  ucum:kelvin ;
    	   {# Any value, will never be used in the scenario. #}
           dul:hasDataValue 280 .
{% endfor %}