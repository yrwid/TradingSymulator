@startuml
class Application
{
  +Run();
}

interface DataRefresher
{
  +virtual RefreshData() = 0;
}

interface Displayer
{
  +virtual DisplayResults() = 0;
}

interface Simulator
{
  +virtual SimulateOn(Data) = 0;
}

class DataRefresherImpl
{
  +virtual RefreshData();
}

class DisplayerImpl
{
  +virtual DisplayResults();
}

class SimulatorImpl
{
  +virtual SimulateOn(Data);
}

interface Collector
{
  +virtual Collect(Period) = 0;
}

interface DataManager
{
  +virtual UpdateIfneccesary(Period) = 0;
  +virtual Read(Period) = 0;
}

class GpwCollector
{
  +virtual Collect(Period);
}

class DataManagerImpl
{
  +virtual UpdateIfneccesary(Period);
  +virtual Read(Period);
}

interface DataControler
{
  +virtual Read(Period) = 0;
  +virtual Save(Period) = 0;
}

class CsvDataControler
{
  +virtual Read(Period);
  +virtual Save(Period);
}

Application <-up- Displayer : Use
Application <-up- Simulator : Use
Application <-up- DataRefresher : Use

Displayer -up-> DisplayerImpl: Implements
Simulator -up-> SimulatorImpl: Implements
DataRefresher -up-> DataRefresherImpl: Implements

DataRefresherImpl <-up- Collector : Use
DataRefresherImpl <-up- DataManager: Use

Collector -up-> GpwCollector: Implements
DataManager -up-> DataManagerImpl : implements

DataManagerImpl <-up- DataControler : Use
DataControler -up-> CsvDataControler: implements

interface Engine
{
  +virtual Run() = 0;
}

class EngineImpl
{
  +virtual Run();
}

interface Strategy
{
  +virtual Calculate() = 0;
}

class SimpleStrategy
{
  +virtual Calculate();
}

interface Statistics
{
  +virtual GetStatistics() = 0;
  +virtual GetSignals() = 0;
}

class SimpleStatistics
{
  +virtual GetStatistics();
  +virtual GetSignals();
}

DataManager --> SimulatorImpl : Use
SimulatorImpl <-up- Engine : Use
Engine -up-> EngineImpl : implements
EngineImpl <-up- Strategy : Use
Strategy -up-> SimpleStrategy : Implements
EngineImpl <-- Statistics : Use
Statistics -up-> SimpleStatistics : Implements
DisplayerImpl <-up- Statistics : Use

interface Display
{
  +virtual Show() = 0;
}

class PlotDisplay
{
  +virtual Show();
}

class TxtDisplay
{
  +virtual Show();
}

DisplayerImpl <-up- Display : Use
Display -up-> PlotDisplay : Implements
Display -up-> TxtDisplay : Implements
@enduml
