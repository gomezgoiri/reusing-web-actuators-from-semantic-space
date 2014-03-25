@prefix dbpedia:  <http://dbpedia.org/resource/> .
@prefix sweet:  <http://sweet.jpl.nasa.gov/> .
@prefix ssn:  <http://www.w3.org/2005/Incubator/ssn/ssnx/ssn#> .

# Heaters with heater actuator
# sth/actuators/heater
{% for heater_name in heater_names %}
@prefix {{ heater_name }}: <http://{{ heater_name }}.net/hvac>.
@prefix {{ heater_name }}act:  <http://{{ heater_name }}.net/hvac/actuators/> .
{% endfor %}


{% for heater_name in heater_names %}
{{ heater_name }}:hvac a dbpedia:HVAC ;
      ssn:attachedSystem {{ heater_name }}act:heater .

{{ heater_name }}act:heater a ssn:Sensor;
  ssn:observes sweet:Temperature ; # In quanTemperature.owl
  ssn:onPlatform {{ heater_name }}:hvac .
{% endfor %}