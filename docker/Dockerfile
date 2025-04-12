FROM ubuntu:jammy-20220531

RUN apt -y update && apt install -y \
  software-properties-common \
  wget \
  g++ gcc cmake \
  python3 \
  pip \
  git \
  default-jdk \
  vim \
  time

RUN pip3 install numpy
RUN pip3 install viennarna

RUN apt install -y python2
RUN apt install -y python2-dev
RUN wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
RUN python2 get-pip.py
RUN pip2 install numpy
RUN pip2 install viennarna

# install ViennaRNA
RUN wget https://www.tbi.univie.ac.at/RNA/download/sourcecode/2_6_x/ViennaRNA-2.6.4.tar.gz
RUN tar -zxvf ViennaRNA-2.6.4.tar.gz && cd ViennaRNA-2.6.4 && ./configure --with-python2 && make && make install 

# install RNAsfbinv
RUN pip3 install rnafbinv
RUN git clone https://github.com/matandro/RNAsfbinv.git

# install RNARedPrint
RUN git clone https://github.com/yannponty/RNARedPrint.git
RUN cd RNARedPrint && make && make install PREFIX='./_inst' && export PATH=`pwd`/_inst/bin:$PATH

# install DesiRNA
RUN git clone https://github.com/fryzjergda/DesiRNA.git
RUN cd DesiRNA && python3 -m pip install -r requirements.txt

# install Modena
RUN wget http://rna.eit.hirosaki-u.ac.jp/modena/multi/v0067b/modena0067b_x86_64.tar.gz && tar -xzvf modena0067b_x86_64.tar.gz 

# install dss-opt
RUN apt install -y libgsl-dev
RUN git clone https://github.com/marcom/dss-opt.git
RUN cd dss-opt && make

# install INFO-RNA
RUN wget http://www.bioinf.uni-freiburg.de/Software/INFO-RNA/versions/INFO-RNA-2.1.2.tar.gz
RUN tar -xzvf INFO-RNA-2.1.2.tar.gz
RUN apt install -y libc6-i386
RUN apt install -y lib32stdc++6

# install MCTS-RNA
RUN git clone https://github.com/tsudalab/MCTS-RNA.git

# install antaRNA
RUN wget http://www.bioinf.uni-freiburg.de/Software/antaRNA/antaRNA_v114.py

RUN pip3 install minineedle

# install RiboLogic
RUN pip2 install networkx numpy matplotlib requests networkx
ENV DEBIAN_FRONTEND=noninteractive
RUN apt -y update && apt install -y python-tk
RUN git clone https://github.com/wuami/RiboLogic.git
ENV VIENNAHOME=/usr/local
ENV NUPACKHOME=/RiboLogic/resources/nupack

# install LEARNA
RUN git clone https://github.com/automl/learna.git
RUN cd learna && make requirements

RUN pip3 install scipy
ENV PATH=/RNARedPrint/_inst/bin:$PATH
RUN echo "echo \"\${1}\" | design-multistate.py --num 100 --gc 0.6 --tolerance=0.5" > /RNARedPrint/design-multistate-helper
RUN chmod +x /RNARedPrint/design-multistate-helper
RUN echo "echo \"\${1}\" > tmp.targets.txt && design-multistate.py -i tmp.targets.txt --num 100 | calcprobs.py -i tmp.targets.txt" > /RNARedPrint/calcprobs-helper
RUN chmod +x /RNARedPrint/calcprobs-helper

# learna has to run from learna dir
WORKDIR /learna
