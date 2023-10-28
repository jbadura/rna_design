FROM ubuntu:jammy-20220531

RUN apt -y update && apt install -y \
  software-properties-common \
  wget \
  g++ gcc cmake \
  python3 \
  pip \
  git \
  default-jdk
  
#RUN add-apt-repository ppa:bibi-help/bibitools

#RUN apt -y update && apt install -y pkiss 

RUN pip install numpy

# install ViennaRNA
RUN wget https://www.tbi.univie.ac.at/RNA/download/sourcecode/2_6_x/ViennaRNA-2.6.4.tar.gz
RUN tar -zxvf ViennaRNA-2.6.4.tar.gz && cd ViennaRNA-2.6.4 && ./configure && make && make install 

# install RNAsfbinv
RUN pip install rnafbinv

# install RNARedPrint
RUN git clone https://github.com/yannponty/RNARedPrint.git
RUN cd RNARedPrint && make && make install PREFIX='./_inst' && export PATH=`pwd`/_inst/bin:$PATH

# install DesiRna
RUN git clone https://github.com/fryzjergda/DesiRNA.git
RUN cd DesiRNA && python3 -m pip install -r requirements.txt && python3 -m pip install viennarna

RUN git clone https://github.com/matandro/RNAsfbinv.git

RUN apt install -y vim

WORKDIR /rna_workdir
